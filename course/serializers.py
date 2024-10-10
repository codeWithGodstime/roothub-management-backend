from rest_framework import serializers

from authentication.serializers import UserSerializer, InstructorSerializer
from authentication.models import Instructor
from .models import Course, CourseSession, CourseSessionPayment


class CourseSession:
    class CourseRetreiveSerializer(serializers.ModelSerializer):
        class Meta:
            model = CourseSession
            fields = ["start_date", "estimated_end_date", "session_info", "is_active", "end_date", "instructors"]

class CourseSerializer:

    class CourseCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = Course
            fields = ["name", "total_amount", "duration"]

    
    class CourseRetrieveSerializer(serializers.ModelSerializer):

        student_count = serializers.SerializerMethodField()
        instructors = serializers.SerializerMethodField()
        active_sessions = serializers.SerializerMethodField()

        class Meta:
            model = Course
            fields = ["id", "name", "total_amount", "duration", "student_count", "instructors", "monthly_amount", "active_sessions"]

        def get_student_count(self, course) -> int:
            return course.students.all().count()

        def get_instructors(self, course):
            # Retrieve all instructors for this course
            instructors = Instructor.objects.filter(
                course_session__course=course
            ).distinct()
            serialized_instructors = InstructorSerializer.InstructorRetrieveSerializer(instructors, many=True)
            return serialized_instructors.data

        def get_active_sessions(self, obj):
            active_course_sessions = obj.sessions.filter(is_active=True)
            serialized_active_course_sessions =  CourseSession.CourseRetreiveSerializer(active_course_sessions, many=True)
            return serialized_active_course_sessions.data