from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail

from .managers import UserManager
from utils.model_mixins import BaseModelMixin


class User(AbstractBaseUser, PermissionsMixin, BaseModelMixin):
    
    email = models.EmailField(unique=True, db_index=True)
    first_name = models.CharField(max_length=300, blank=False, null=True)
    last_name = models.CharField(max_length=300, blank=False, null=True)

    is_instructor = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    class Meta:
        ordering = ["-created_at"]

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        # send_mail(subject, message, from_email, [self.email], fail_silently=True, **kwargs) #TODO: fix email is not sending 
        send_mail(subject, message, from_email, [self.email], fail_silently=True, **kwargs) #TODO: fix email is not sending 


class Instructor(BaseModelMixin):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, related_name="instructor")


class Student(BaseModelMixin):

    type = {t: t for t in ["INTERN", "EXTERN"]}
    payment_status = {p:p for p in ['FULL', "PART", "NOT PAID"]}

    user = models.OneToOneField(User, related_name="student", on_delete=models.DO_NOTHING)
    address = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=11) #TODO change to a standard number like 1234 000 000 000 format
    has_paid = models.BooleanField(default=False)
    date_of_payment = models.DateField()
    commencement_date = models.DateField()
    #TODO: from the amount paid calculate the number of month paid
    amount_paid = models.DecimalField(decimal_places=2, max_digits=14)
    course = models.ForeignKey("Course", models.DO_NOTHING)
    number_of_presentation = models.PositiveIntegerField(default=0)
    payment_status = models.CharField(max_length=20, choices=payment_status)
    type = models.CharField(max_length=300, choices=type)
    course_session = models.ForeignKey("CourseSession", models.DO_NOTHING, related_name="students")


class StudentPresentation(BaseModelMixin):
    student = models.ForeignKey(Student, models.DO_NOTHING, related_name="presentations")
    previous_presentation_date = models.DateField()
    next_presentation_date = models.DateField(null=True, blank=True)


class Course(BaseModelMixin):
    ...


class CourseSession(BaseModelMixin):
    ...


