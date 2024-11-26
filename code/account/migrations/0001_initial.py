# Generated by Django 4.0 on 2024-11-22 22:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserOffDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('off_day', models.DateField(help_text='Off Day', verbose_name='Off Day')),
                ('end_off_day', models.DateField(blank=True, help_text='End Off Day', null=True, verbose_name='End Off Day')),
                ('off_day_type', models.CharField(help_text='Off Day Type', max_length=50, verbose_name='Off Day Type')),
                ('user', models.ForeignKey(help_text='User', on_delete=django.db.models.deletion.CASCADE, related_name='off_days', to='auth.user', verbose_name='User')),
            ],
            options={
                'verbose_name': 'User Off Day',
                'verbose_name_plural': 'User Off Days',
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('annual_leave', models.FloatField(default=15, help_text='Annual Leave', verbose_name='Annual Leave')),
                ('user_start_time', models.DateTimeField(blank=True, help_text='User Start Work', null=True, verbose_name='User Tracking')),
                ('user_end_time', models.DateTimeField(blank=True, help_text='User End Work', null=True, verbose_name='User Tracking')),
                ('status', models.BooleanField(default=False, help_text='User Work Status')),
                ('user', models.OneToOneField(blank=True, help_text='User', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='info', to='auth.user', verbose_name='User')),
            ],
            options={
                'verbose_name': 'User Info',
                'verbose_name_plural': 'User Info',
            },
        ),
    ]
