from django.contrib import admin
from .models import UserInfo, OffRequest, UserOffDay, UserWorkTime, Notification

admin.site.register(UserInfo)
admin.site.register(UserOffDay)
admin.site.register(UserWorkTime)
admin.site.register(OffRequest)
admin.site.register(Notification)
