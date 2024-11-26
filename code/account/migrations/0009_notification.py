# Generated by Django 4.0 on 2024-11-25 19:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('account', '0008_alter_offrequest_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_key', models.CharField(choices=[('Geç Kaldı', 'Geç Kaldı'), ('İzin Azaldı', 'İzin Azaldı')], help_text='Type', max_length=50, verbose_name='Type')),
                ('seen_status', models.BooleanField(default=False, help_text='Seen Status', verbose_name='Seen Status')),
                ('user', models.ForeignKey(help_text='User', on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='auth.user', verbose_name='User')),
            ],
            options={
                'verbose_name': 'Notification',
                'verbose_name_plural': 'Notifications',
            },
        ),
    ]