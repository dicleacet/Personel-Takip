from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('login_staff/', views.login_staff, name='login_staff'),
    path('staff_dashboard/', views.home_staff, name='staff_dashboard'),
    path('logout_staff/', views.logout_staff, name='logout_staff'),
    path('accept_off_request/<int:id>/', views.accept_off_request, name='accept_off_request'),
    path('reject_off_request/<int:id>/', views.reject_off_request, name='reject_off_request'),
    path('unread_notification/<str:session_key>/', views.get_unread_notification, name='unread_notification'),
    path('read_notification/', views.read_notification, name='read_notification'),
    ]


