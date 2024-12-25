from datetime import date, timedelta
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail

from .managers import UserManager
from utils.model_mixins import BaseModelMixin
# from course.models import Course, CourseSession


class User(AbstractBaseUser, PermissionsMixin, BaseModelMixin):
    RELATIONSHIPS = (
        ("SISTER", "sister"),
        ("BROTHER", "brother"),
        ("FATHER", "father"),
        ("MOTHER", "mother"),
        ("SON", "son"),
        ("DAUGHTER", "daughter"),
        ("FRIEND", "friend"),
        ("PARTNER", "partner"),
        ("COLLEAGUE", "colleague"),
    )

    email = models.EmailField(unique=True, db_index=True)
    first_name = models.CharField(max_length=300, blank=False, null=False)
    last_name = models.CharField(max_length=300, blank=False, null=False)
    home_address = models.CharField(max_length=200)

    is_instructor = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    next_of_kin_contact = models.CharField(
        max_length=20, blank=False, null=False)
    next_of_kin_email = models.EmailField(blank=False, null=False)
    next_of_kin_name = models.CharField(
        max_length=200, blank=False, null=False)
    next_of_kin_relationship = models.CharField(
        max_length=20, choices=RELATIONSHIPS, blank=False, null=False
    )

    USERNAME_FIELD = "email"

    objects = UserManager()

    class Meta:
        ordering = ["-created_at"]

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        # send_mail(subject, message, from_email, [self.email], fail_silently=True, **kwargs) #TODO: fix email is not sending
        send_mail(subject, message, from_email, [
                  self.email], fail_silently=True, **kwargs)  # TODO: fix email is not sending


class Program(BaseModelMixin):
    """ A program is a course that has multiple sub-courses that can taught by different instructors """

    DURATION_CHOICES = [
        (1, "1 Month"),
        (2, "2 Months"),
        (3, "3 Months"),
        (4, "4 Months"),
    ]

    name = models.CharField(max_length=300, unique=True)
    duration = models.PositiveIntegerField(choices=DURATION_CHOICES)
    total_amount = models.DecimalField(max_digits=16, decimal_places=2)


class Instructor(BaseModelMixin):
    user = models.OneToOneField(
        User, on_delete=models.DO_NOTHING, related_name="instructor")
    skills = models.JSONField(default=list)
    account_number = models.CharField(max_length=30, null=True, blank=True)
    account_name = models.CharField(max_length=100, null=True, blank=True)
    bank_name = models.CharField(max_length=200, null=True, blank=True)

class InstructorSkill(BaseModelMixin):
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, unique=True)
    is_primary = models.BooleanField(default=False)

class Student(BaseModelMixin):

    type = {t: t for t in ["INTERN", "EXTERN", "TRIPTERN"]}
    payment_plan = {p: p for p in ['FULL', "PART", "NOT PAID"]}

    user = models.OneToOneField(
        User, related_name="student", on_delete=models.DO_NOTHING)
    type = models.CharField(max_length=300, choices=type)
    payment_plan = models.CharField(max_length=30, choices=payment_plan)
    program = models.ForeignKey(
        Program, related_name="students", on_delete=models.RESTRICT)
    courses = models.ManyToManyField("course.Course", through="course.StudentCourse", related_name="students")


class StudentPayment(BaseModelMixin):

    amount = models.DecimalField(decimal_places=2, max_digits=16)
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    payment_date = models.DateField()


# class StudentCourseSession(BaseModelMixin):
#     student = 