from django.db import models
from django.contrib.auth.models import User

izin_onay = (
    ('Onaylandı', 'Onaylandı'),
    ('Reddedildi', 'Reddedildi'),
    ('Beklemede', 'Beklemede'),
)

class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="info",
                                null=True, blank=True, verbose_name="User", help_text="User")
    annual_leave = models.FloatField(default=15, verbose_name="Annual Leave", help_text="Annual Leave")

    class Meta:
        verbose_name = "User Info"
        verbose_name_plural = "User Info"


class UserWorkTime(models.Model):
    work_day = models.DateField(verbose_name="Work Day", help_text="Work Day", null=True, blank=True)
    user_start_time = models.TimeField(verbose_name="User Start Work", help_text="User Start Work", null=True,
                                           blank=True)
    user_end_time = models.TimeField(verbose_name="User End Work", help_text="User End Work", null=True, blank=True)
    late = models.BooleanField(default=False, verbose_name="Late", help_text="Late")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="work_time", verbose_name="User",
                             help_text="User")
    status = models.BooleanField(default=False, help_text="User Work Status")

    class Meta:
        verbose_name = "User Work Time"
        verbose_name_plural = "User Work Times"


class UserOffDay(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="off_days", verbose_name="User",
                             help_text="User")
    off_day = models.DateField(verbose_name="Off Day", help_text="Off Day")
    end_off_day = models.DateField(verbose_name="End Off Day", help_text="End Off Day", null=True, blank=True)
    off_day_type = models.CharField(max_length=50, verbose_name="Off Day Type", help_text="Off Day Type")

    class Meta:
        verbose_name = "User Off Day"
        verbose_name_plural = "User Off Days"


class OffRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="off_requests", verbose_name="User",
                             help_text="User")
    off_day = models.DateField(verbose_name="Off Day", help_text="Off Day")
    end_off_day = models.DateField(verbose_name="End Off Day", help_text="End Off Day", null=True, blank=True)
    off_day_type = models.CharField(max_length=50, verbose_name="Off Day Type", help_text="Off Day Type")
    status = models.izin_onay = models.CharField(max_length=50, choices=izin_onay, default='Beklemede',
                                                verbose_name="Status", help_text="Status")

    class Meta:
        verbose_name = "Off Request"
        verbose_name_plural = "Off Requests"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications", verbose_name="User",
                             help_text="User")
    type_key = models.CharField(max_length=50, verbose_name="Type", help_text="Type")
    seen_status = models.BooleanField(default=False, verbose_name="Seen Status", help_text="Seen Status")

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
