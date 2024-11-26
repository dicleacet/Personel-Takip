from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from account.models import UserInfo

class Command(BaseCommand):
    help = "Creates 'Yöneticiler' and 'Kullanıcılar' groups, 2 regular users, and 2 users in the 'Yöneticiler' group."

    def handle(self, *args, **kwargs):
        # Create groups
        admin_group_name = "Yöneticiler"
        user_group_name = "Kullanıcılar"

        admin_group, created_admin = Group.objects.get_or_create(name=admin_group_name)
        if created_admin:
            self.stdout.write(self.style.SUCCESS(f"Group '{admin_group_name}' created successfully."))
        else:
            self.stdout.write(self.style.WARNING(f"Group '{admin_group_name}' already exists."))

        user_group, created_user = Group.objects.get_or_create(name=user_group_name)
        if created_user:
            self.stdout.write(self.style.SUCCESS(f"Group '{user_group_name}' created successfully."))
        else:
            self.stdout.write(self.style.WARNING(f"Group '{user_group_name}' already exists."))

        # User data
        users = [
            {"username": "user1", "email": "user1@example.com", "password": "user1pass", "is_admin": False},
            {"username": "user2", "email": "user2@example.com", "password": "user2pass", "is_admin": False},
            {"username": "admin1", "email": "admin1@example.com", "password": "admin1pass", "is_admin": True},
            {"username": "admin2", "email": "admin2@example.com", "password": "admin2pass", "is_admin": True},
        ]

        # Create users
        for user_data in users:
            if User.objects.filter(username=user_data["username"]).exists():
                self.stdout.write(self.style.WARNING(f"User '{user_data['username']}' already exists."))
            else:
                user = User.objects.create_user(
                    username=user_data["username"],
                    email=user_data["email"],
                    password=user_data["password"],
                )
                if user_data["is_admin"]:
                    user.groups.add(admin_group)
                else:
                    user.groups.add(user_group)
                    UserInfo.objects.create(user=user)

                self.stdout.write(self.style.SUCCESS(f"User '{user_data['username']}' created successfully."))

        self.stdout.write(self.style.SUCCESS("All users and groups setup completed."))
