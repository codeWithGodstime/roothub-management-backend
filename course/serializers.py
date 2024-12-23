from rest_framework import serializers

from authentication.models import Instructor
from .models import Course, CourseSession


class CourseSerializer:

    class CourseCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = Course
            fields = [
                "name", 
                "program", 
                "instructor", 
                "duration"
            ]

    class CourseRetrieveSerializer(serializers.ModelSerializer):

        class Meta:
            model = Course
            fields = [
                "id", 
                "name", 
                "program",
                "duration",  
                "instructor", 
                "level"
            ]
    
    class AssignInstructorToCourse(serializers.ModelSerializer):
        instructor_id = serializers.PrimaryKeyRelatedField(queryset=Instructor.objects.all())

        class Meta:
            model = Course
            fields = [
                "instructor_id"
            ]
        
        def save(self):
            course = self.context.get("course")
            instructor = self.validated_data["instructor_id"]

            # Assign the instructor to the course
            course.instructor = instructor
            course.save()
            return course


class CourseSessionSerializer:
    class CourseSessionCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = CourseSession
            fields = ['start_date', "course"]

    class CourseSessionRetrieveSerializer(serializers.ModelSerializer):
        class Meta:
            model = CourseSession
            fields = "__all__"