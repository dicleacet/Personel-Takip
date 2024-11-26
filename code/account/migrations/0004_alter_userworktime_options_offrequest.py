# Generated by Django 4.0 on 2024-11-24 03:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('account', '0003_userworktime_late'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userworktime',
            options={'verbose_name': 'User Work Time', 'verbose_name_plural': 'User Work Times'},
        ),
        migrations.CreateModel(
            name='OffRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('off_day', models.DateField(help_text='Off Day', verbose_name='Off Day')),
                ('end_off_day', models.DateField(blank=True, help_text='End Off Day', null=True, verbose_name='End Off Day')),
                ('off_day_type', models.CharField(help_text='Off Day Type', max_length=50, verbose_name='Off Day Type')),
                ('status', models.BooleanField(default=False, help_text='Off Request Status')),
                ('user', models.ForeignKey(help_text='User', on_delete=django.db.models.deletion.CASCADE, related_name='off_requests', to='auth.user', verbose_name='User')),
            ],
            options={
                'verbose_name': 'Off Request',
                'verbose_name_plural': 'Off Requests',
            },
        ),
    ]
