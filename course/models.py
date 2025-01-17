from django.db import models
from utils.model_mixins import BaseModelMixin
from django.db.models import UniqueConstraint


class Course(BaseModelMixin):
    name = models.CharField(max_length=300, unique=True)
    instructor = models.ForeignKey(
        'authentication.Instructor',
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
    )  # 4weeks
    level = models.CharField(
        max_length=2,
        choices=((str(i), i) for i in range(1, 5))
    )  # 4weeks


class CourseSession(BaseModelMixin):
    start_date = models.DateTimeField(null=True, blank=True)
    estimated_end_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    course = models.ForeignKey(
        Course,
        related_name='sessions',
        on_delete=models.CASCADE
    )
    is_active = models.BooleanField(default=False)

    def get_instructor(self):
        """should get instructor fullname"""
        return self.course.user.fullname()


class StudentCourse(BaseModelMixin):
    # m2m for student and course e.g student can offer graphics-beginner, advanced
    student = models.ForeignKey(
        "authentication.Student", on_delete=models.RESTRICT)
    course = models.ForeignKey('course.Course', on_delete=models.RESTRICT)

    class Meta:
        constraints = [
            # to enforce that student cannout be part of a course multiple times
            UniqueConstraint(fields=['student', 'course'],
                             name='unique_student_course')
        ]


class StudentCourseSession(BaseModelMixin):
    """This is used to track the current session the student is on"""
    student_course = models.ForeignKey(
        StudentCourse,
        on_delete=models.RESTRICT,
        related_name="sessions"
    )
    course_session = models.ForeignKey(
        "course.CourseSession",
        on_delete=models.RESTRICT,
        related_name="student_sessions"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student_course', 'course_session'],
                name='unique_student_course_session'
            )
        ]
