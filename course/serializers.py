from rest_framework import serializers

from authentication.serializers import UserSerializer
from authentication.models import Instructor
from .models import Course


class CourseSerializer:

    class CourseCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = Course
            fields = ["name", "total_amount", "duration"]

    
    class CourseRetrieveSerializer(serializers.ModelSerializer):

        student_count = serializers.SerializerMethodField()
        instructors = serializers.SerializerMethodField()

        class Meta:
            model = Course
            fields = ["name", "total_amount", "duration", "student_count", "instructors"]

        def get_student_count(self, course) -> int:
            return course.students.all().count()

        def get_instructors(self, course):
            # Retrieve all instructors for this course
            instructors = Instructor.objects.filter(
                coursetutor__course_session__course=course
            ).distinct()
            serialized_instructors = UserSerializer.InstructorUserRetrieveSerializer(instructors, many=True)
            return serialized_instructors.data