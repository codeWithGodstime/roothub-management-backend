from celery import shared_task
from celery.utils.log import get_task_logger

from django.contrib.auth import get_user_model
from django.core.mail import send_mass_mail

from .models import Announcement

User = get_user_model()

logger = get_task_logger(__name__)


@shared_task
def send_announcement_email(announcement_id):
    try:
        announcement = Announcement.objects.get(id=announcement_id)
        # fetch all user based on that receiver role
        users = User.objects.all()

        if announcement.receiver_group == "ALL":
            users = users.filter(is_superuser=False).values("email")
        elif announcement.receiver_group == "TRAINER":
            users = users.filter(is_instructor=True).values("email")
        elif announcement.receiver_group == "TRAINEE":
            users = users.filter(is_student=True).values("email")

        receipient_list = [user["email"] for user in users]
        print(receipient_list, "===")
        if receipient_list:
            data = (
                (
                    announcement.title,
                    announcement.message,
                    "admin@roothub.com",
                    receipient_list,
                ),
            )

            send_mass_mail(data, fail_silently=False)
            announcement.save()
    except Announcement.DoesNotExist:
        pass
