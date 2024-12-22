from rest_framework import serializers

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


class CourseSessionSerializer:
    class CourseSessionCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = CourseSession
            fields = ['start_date', "course"]

    class CourseSessionRetrieveSerializer(serializers.ModelSerializer):
        class Meta:
            model = CourseSession
            fields = "__all__"