from datetime import date, timedelta
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail

from .managers import UserManager
from utils.model_mixins import BaseModelMixin


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

    next_of_kin_contact = models.CharField(max_length=40, blank=False, null=False)
    next_of_kin_email = models.EmailField(blank=False, null=False)
    next_of_kin_name = models.CharField(max_length=200, blank=False, null=False)
    next_of_kin_relationship = models.CharField(
        max_length=40, choices=RELATIONSHIPS, blank=False, null=False
    )

    USERNAME_FIELD = "email"

    objects = UserManager()

    class Meta:
        ordering = ["-created_at"]

    @property
    def fullname(self):
        return f"{self.first_name} {self.last_name}"

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        # send_mail(subject, message, from_email, [self.email], fail_silently=True, **kwargs) #TODO: fix email is not sending
        send_mail(
            subject,
            message,
            from_email,
            [
                # TODO: fix email is not sending in production
                self.email
            ],
            fail_silently=True,
            **kwargs,
        )


class Program(BaseModelMixin):
    """A program is a course that has multiple sub-courses that can taught by different instructors"""

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
        User, on_delete=models.CASCADE, related_name="instructor"
    )
    account_number = models.CharField(max_length=50, null=True, blank=True)
    account_name = models.CharField(max_length=100, null=True, blank=True)
    bank_name = models.CharField(max_length=200, null=True, blank=True)
    skills = models.ManyToManyField("Skill", through="InstructorSkill")

    def __str__(self):
        return self.user.email

    @classmethod
    def filter_by_skills(cls, skill_name):
        """get all instructors with have a particular skill"""
        return cls.objects.filter(skills__name=skill_name)


class Skill(BaseModelMixin):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class InstructorSkill(BaseModelMixin):
    instructor_id = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    skill_id = models.ForeignKey(Skill, on_delete=models.CASCADE)
    is_primary = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["instructor_id", "is_primary"],
                name="single_instructor_primary_skill",
            ),
             # Ensure each skill is unique per instructor (with or without primary)
            models.UniqueConstraint(
                fields=["instructor_id", "skill_id"],
                name="unique_instructor_skill",
            ),
        ]

    # def clean(self):
    #     # Ensure no duplicate primary skills for the same instructor
    #     if self.is_primary and self.instructor_id.skills.filter(is_primary=True).exists():
    #         raise models.ValidationError("An instructor can only have one primary skill.")


class Student(BaseModelMixin):

    type = {t: t for t in ["INTERN", "EXTERN", "TRIPTERN"]}
    payment_plan = {p: p for p in ["FULL", "PART", "NOT PAID"]}

    user = models.OneToOneField(User, related_name="student", on_delete=models.CASCADE)
    type = models.CharField(max_length=300, choices=type)
    payment_plan = models.CharField(max_length=40, choices=payment_plan)
    program = models.ForeignKey(
        Program, related_name="students", on_delete=models.RESTRICT
    )
    courses = models.ManyToManyField(
        "course.Course", through="course.StudentCourse", related_name="students"
    )
    session = models.ForeignKey(
        "course.CourseSession",
        related_name="students",
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
    )  # student can exist without been assigned to a course

    @property
    def get_latest_tutor(self):
        # Get the latest course the student is enrolled in (using the StudentCourse through model)
        latest_course = self.courses.order_by("studentcourse__created_at").last()

        if latest_course and latest_course.instructor:
            # Return the instructor (tutor) for the latest course
            return latest_course.instructor.user.fullname
        return None  # Return None if no tutor found or no course is found

    @property
    def get_latest_level(self):
        # Get the latest course the student is enrolled in from the many-to-many relationship
        latest_course = self.courses.order_by("-studentcourse__created_at").first()

        if latest_course:
            return latest_course.level
        return None  # Return None if no course found


class StudentPayment(BaseModelMixin):
    amount = models.DecimalField(decimal_places=2, max_digits=16)
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    payment_date = models.DateField()
