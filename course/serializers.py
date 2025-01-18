from rest_framework import serializers

from authentication.models import Instructor, Student
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
        # course = serializers.SerializerMethodField()
        class Meta:
            model = CourseSession
            fields = [
                "id",
                "start_date",
                "estimated_end_date",
                "end_date",
                # "course",
                "is_active",
                "created_at",
                "updated_at"
            ]

        # def get_course(self, obj):
        #     return obj.course.name

    class AddStudentToSessionSerializer(serializers.Serializer):
        student_id = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())

        def validate(self, data):
            student = data.get('student_id')
            session = self.context.get("session")

            # Check if the student is already associated with the session
            if Student.objects.filter(id=student.id, session=session).exists():
                raise serializers.ValidationError("The student is already added to this session.")
            return data

        def save(self, **kwargs):
            student = self.validated_data['student_id']
            student.session = self.context.get("session")
            student.save()
            return student