from rest_framework import serializers

from authentication.models import Instructor, Student
from .models import Course, CourseSession, StudentCourseSession, StudentCourse


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

    class AddStudentCourseSessionSession(serializers.ModelSerializer):

        student_id = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
        class Meta:
            model = CourseSession
            fields = ["student_id"]

        def save(self, **kwargs):
            session = self.context.get("session")  # Get the session instance from the context
            student = self.validated_data["student_id"]
            print(session, "==sesssion")

            # Add the student to the session's many-to-many relationship
            session.students.add(student)
            return session

# class StudentCourseSessionSerializer:
#     class StudentCourseSessionCreateSerializer(serializers.ModelSerializer):
#         class Meta:
#             model = StudentCourseSession
#             fields = ["student", "course"]
        
    
#     class StudentCourseSessionRetrieveSerializer(serializers.ModelSerializer):
#         class Meta:
#             model = StudentCourseSession
#             fields = ["student", "course", "created_at", "updated_at"]