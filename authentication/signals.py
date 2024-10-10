from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Student

@receiver(post_save, sender=Student)
def add_student_course_session(sender, instance, created, *args, **kwargs):
    if created:
        instance.add_student_to_session()