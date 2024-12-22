from django.db import models
from utils.model_mixins import BaseModelMixin


class Course(BaseModelMixin):
    name = models.CharField(max_length=300, unique=True)
    instructor = models.OneToOneField(
        'authentication.User', 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL
    )
    program = models.ForeignKey(
        "authentication.Program", 
        related_name="courses",
        on_delete=models.CASCADE
    )
    duration = models.CharField(
        max_length=2, 
        choices=((str(i), i) for i in range(1, 5))
    ) #4weeks
    level = models.CharField(
        max_length=2, 
        choices=((str(i), i) for i in range(1, 5))
    ) #4weeks


class CourseSession(BaseModelMixin):
    start_date = models.DateTimeField(null=True, blank=True)
    estimated_end_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    course = models.ForeignKey(
        Course, 
        related_name='sessions', 
        on_delete=models.CASCADE
    )
    is_active = models.BooleanField(default=True)