import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Course, CourseSession

logger = logging.getLogger(__file__)

@receiver(post_save, sender=Course) 
def create_session_for_course(sender, instance, created, **kwargs):
    
    if created:
        session = CourseSession.objects.create(
            course = instance,
        )
        session.save()
    
        logger.info(f"Session {session.id} was created for {instance.id}")
