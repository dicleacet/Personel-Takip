import json
from datetime import datetime, timedelta, time
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.sessions.models import Session
from .decorators import group_check
from django.contrib.auth import authenticate, login, logout
from .models import UserInfo, UserOffDay, UserWorkTime, OffRequest, Notification
import logging
from app.celery import create_notification

work_start_time = time(8, 0, 0)
work_end_time = time(18, 0, 0)
hours_of_day = 8

logger = logging.getLogger("pt")


def index(request):
    return render(request, 'index.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        now = datetime.now()
        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if not UserWorkTime.objects.filter(user=user, work_day=now.date()).exists():
                    UserWorkTime.objects.create(user=user, user_start_time=now.time(), work_day=now.date(), status=True)
                    if now.time() > work_start_time:
                        create_notification.delay(user.id, 'late')
                        UserWorkTime.objects.filter(user=user).update(late=True)
                        late_hours = now.hour - work_start_time.hour
                        if late_hours >= 1:
                            late_rate = late_hours / hours_of_day
                            user_info = UserInfo.objects.get(user=user)
                            user_info.annual_leave -= late_rate
                            user_info.save()
                            if user_info.annual_leave < 3:
                                create_notification.delay(user.id, 'annual leave')
                else:
                    messages.info(request, 'You have already logged in')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Please enter username and password')

    return render(request, 'user/login.html')


def logout_view(request):
    UserWorkTime.objects.filter(user=request.user, work_day=datetime.now().date()).update(user_end_time=datetime.now().time())
    logout(request)
    return redirect('login')


@login_required(login_url='/login/')
def home(request):
    if request.user.groups.filter(id=1).exists():
        return redirect('staff_dashboard')

    if request.method == 'POST':
        off_day = request.POST.get('off_day')
        end_off_day = request.POST.get('end_off_day')
        off_day_type = request.POST.get('off_day_type')
        if off_day and off_day_type and end_off_day:
            if datetime.strptime(off_day, '%Y-%m-%d') > datetime.strptime(end_off_day, '%Y-%m-%d'):
                messages.error(request, 'End off day must be greater than off day')
            else:
                OffRequest.objects.create(user=request.user, off_day=off_day, end_off_day=end_off_day,
                                          off_day_type=off_day_type)
                messages.success(request, 'Off day request has been sent')
        else:
            messages.error(request, 'Please fill all fields')
    user_off_request = OffRequest.objects.filter(user=request.user)
    return render(request, 'user/home.html', {'user_off_request': user_off_request})


def login_staff(request):
    if request.user.is_authenticated and group_check(1):
        return redirect('staff_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                if group_check(1):
                    login(request, user)
                else:
                    messages.error(request, 'You are not authorized to login')
                return redirect('staff_dashboard')
            else:
                messages.error(request, 'Invalid username or password')

    return render(request, 'staff/login.html')


@group_check(1)
@login_required(login_url='/login_staff/')
def home_staff(request):
    lates_user = []
    lates = UserWorkTime.objects.filter(late=True, work_day=datetime.now().date())
    for late in lates:
        late_minute = datetime.combine(datetime.now().date(), late.user_start_time) - datetime.combine(
            datetime.now().date(), work_start_time)
        if late_minute > timedelta(minutes=1):
            lates_user.append({
                'user': late.user,
                'late_minute': late_minute
            })

    users = []
    for user in User.objects.all():
        if user.groups.filter(id=2).exists():
            users.append(
                {
                    'user': user,
                    'work_status': UserWorkTime.objects.filter(user=user, work_day=datetime.now().date()).first()
                }
            )
    off_requests = OffRequest.objects.filter(status='Beklemede')
    notification = Notification.objects.filter(seen_status=False)
    return render(request, 'staff/home.html',
                  {"user_off": UserOffDay.objects.all(),
                   'lates_user': lates_user,
                   'users': users,
                   'off_requests': off_requests,
                   'Notifications': notification})


def logout_staff(request):
    logout(request)
    return redirect('login_staff')


def accept_off_request(request, id):
    off_request = OffRequest.objects.get(id=id)
    off_request.status = 'Onaylandı'
    off_request.save()
    return redirect('staff_dashboard')


def reject_off_request(request, id):
    off_request = OffRequest.objects.get(id=id)
    off_request.status = 'Reddedildi'
    off_request.save()
    return redirect('staff_dashboard')


def get_unread_notification(request, session_key):
    session = Session.objects.filter(session_key=session_key).first()
    notifications_count = 0
    if session:
        user_id = int(session.get_decoded()['_auth_user_id'])
        if User.objects.filter(id=user_id).exists() and Group.objects.filter(id=1).exists():
            notifications = Notification.objects.filter(seen_status=False)
            notifications_count = notifications.count()

    return JsonResponse({'status': 'success', "count": notifications_count})


def read_notification(request):
    if request.method == 'POST':
        data = request.POST.get('notification_ids')
        data = json.loads(data)
        for id in data:
            Notification.objects.filter(id=id).update(seen_status=True)
        messages.success(request, 'Notifications have been read')
        return JsonResponse({'status': 'success', 'data': data})
