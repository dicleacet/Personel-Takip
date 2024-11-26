import os
import django
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

redis_host = os.environ.get("REDIS_HOST", "localhost")  # Default localhost
redis_port = os.environ.get("REDIS_PORT", "6379")      # Default 6379
celery_app = Celery('app', broker=f"redis://{redis_host}:{redis_port}/0")


@celery_app.task
def create_notification(user_id: int, type_key: str):
    from account.models import Notification
    try:
        Notification.objects.create(user_id=user_id, type_key=type_key)
        return "Notification created successfully"
    except Exception as e:
        return f"Error creating notification: {e}"


