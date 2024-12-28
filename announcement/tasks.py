import logging
from celery import shared_task
from celery.utils.log import get_task_logger

from django.contrib.auth import get_user_model
from django.core.mail import send_mass_mail

from .models import Announcement

User = get_user_model()

logger = get_task_logger(__name__)

@shared_task
def send_announcement_email(announcement_id):
    logger.info(f"Starting to process email sending for announcement ID: {announcement_id}")
    try:
        announcement = Announcement.objects.get(id=announcement_id)
        logger.info(f"Announcement fetched: {announcement.title} (ID: {announcement_id})")
        
        # Fetch all users based on the receiver role
        users = User.objects.all()
        if announcement.receiver_group == "ALL":
            users = users.filter(is_superuser=False).values("email")
            logger.info("Targeting all non-superuser users for the email.")
        elif announcement.receiver_group == "TRAINER":
            users = users.filter(is_instructor=True).values("email")
            logger.info("Targeting trainers for the email.")
        elif announcement.receiver_group == "TRAINEE":
            users = users.filter(is_student=True).values("email")
            logger.info("Targeting trainees for the email.")

        recipient_list = [user["email"] for user in users]
        logger.debug(f"Recipient list: {recipient_list}")

        if recipient_list:
            data = [
                (
                    announcement.title,
                    announcement.message,
                    "admin@roothub.com",
                    [user_email],
                )
                for user_email in recipient_list
            ]
            logger.info(f"Prepared {len(data)} email(s) for sending.")
            
            try:
                send_mass_mail(data, fail_silently=False)
                logger.info(f"Successfully sent {len(data)} email(s) for announcement ID: {announcement_id}")
            except Exception as e:
                logger.error(f"Failed to send emails for announcement ID: {announcement_id}. Error: {e}")

            announcement.save()
        else:
            logger.warning(f"No recipients found for announcement ID: {announcement_id}")

    except Announcement.DoesNotExist:
        logger.error(f"Announcement with ID {announcement_id} does not exist.")
    except Exception as e:
        logger.exception(f"An unexpected error occurred while sending emails for announcement ID: {announcement_id}. Error: {e}")