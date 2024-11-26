from django.contrib.auth.models import Group
from django.shortcuts import redirect


def group_check(group_id):
    def method_wrap(view_method):
        def wrap(request, *args, **kwargs):
            status = False
            permissions = Group.objects.filter(id=group_id, user=request.user)
            if permissions:
                status = True
            elif request.user.is_staff:
                status = True
            else:
                status = False
            if status == False:
                return redirect('home')
            return view_method(request, *args, **kwargs)
        return wrap
    return method_wrap
