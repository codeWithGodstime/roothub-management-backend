from decimal import Decimal
from django.db import models
from utils.model_mixins import BaseModelMixin

"""
A course represents a general learning path with a name, duration, and payment details.
A course session represents a particular occurrence of a course (e.g., the same course taught at different times or terms).
A tutor (or instructor) can teach a course, but you want to keep track of which tutor taught which course session, as the same course might have different instructors in different sessions.

"""

# Define Duration Choices
DURATION_CHOICES = [
    ('1', '1 month'),
    ('2', '2 months'),
    ('3', '3 months'),
    ('4', '4 months'),
]

class Course(BaseModelMixin):
    """Represents a Course, its pricing, and duration."""
    name = models.CharField(max_length=300)
    total_amount = models.DecimalField(decimal_places=2, max_digits=16)
    monthly_amount = models.DecimalField(decimal_places=2, max_digits=16, null=True, blank=True)
    duration = models.CharField(max_length=1, choices=DURATION_CHOICES)

    def calculate_monthly_amount(self):
        duration = Decimal(self.duration) if self.duration.isdigit() else 1
        return self.total_amount / duration

    def save(self, *args, **kwargs):
        self.monthly_amount = self.calculate_monthly_amount()
        return super().save(*args, **kwargs)


class CourseSession(BaseModelMixin):
    """Represents a specific session of a course, which may have different instructors."""
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, related_name="sessions")  # Each session belongs to one course
    start_date = models.DateField()
    estimated_end_date = models.DateField()
    session_info = models.JSONField(default=dict)
    is_active = models.BooleanField(default=False)
    end_date = models.DateField()
    instructors = models.ManyToManyField(
        "authentication.Instructor", through="CourseTutor", related_name="course_sessions"
    )  # Many instructors can teach many sessions


class CourseTutor(BaseModelMixin):
    """Represents the relationship between an instructor and a course session."""
    instructor = models.ForeignKey("authentication.Instructor", on_delete=models.DO_NOTHING)
    course_session = models.ForeignKey(CourseSession, on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = ("instructor", "course_session")


class CourseSessionPayment(BaseModelMixin):
    """when an instructor is paid, would be added here"""
    instructor = models.ForeignKey("authentication.Instructor", on_delete=models.DO_NOTHING)
    course_session = models.OneToOneField(CourseSession, on_delete=models.DO_NOTHING) 
    amount = models.DecimalField(max_digits=16, decimal_places=2)

    class Meta:
        unique_together = ("instructor", "course_session") # so an instructor can be paid only once