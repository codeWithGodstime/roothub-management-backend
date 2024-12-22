from rest_framework import serializers

from .models import Course


# class CourseSessionSerializer:
#     class CourseSessionRetreiveSerializer(serializers.ModelSerializer):

#         number_of_students = serializers.SerializerMethodField()

#         class Meta:
#             model = CourseSession
#             fields = ["id", "start_date", "estimated_end_date", "session_info", "is_active", "end_date", "instructors", "number_of_students"]

#         def get_number_of_students(self, obj):
#             return obj.get_session_students().count()

#     class CourseSessionUnassignedSerializer(serializers.ModelSerializer):
#         """all sessions without instructors"""

#         course = serializers.StringRelatedField()
#         has_instructor = serializers.SerializerMethodField()

#         class Meta:
#             model = CourseSession
#             fields = ("course", "has_instructor")

#         def get_has_instructor(self, obj):
#             pass

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
            ]


    

    