from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from django.db import transaction
from django.db.utils import IntegrityError
from faker import Faker

from authentication.models import User, Instructor, InstructorSkill, Student, StudentPayment, Program
from authentication.tests.factories.instruction_factory import *
from authentication.tests.factories.program_factory import *
from authentication.tests.factories.student_factory import *
from authentication.tests.factories.user_factory import *

from course.models import Course
from course.tests.factories.course_factory import *
from course.tests.factories.coursesession_factory import *

from announcement.models import Announcement
from announcement.tests.factories.announcement_factory import *

fake = Faker()


class GenerateSerializer(serializers.Serializer):
    model = serializers.ChoiceField(
        choices=[
            ('courses', 'courses'),
            ('users', 'users'),
            ('instructors', 'instructors'),
            ('students', 'students'),
            ('programs', 'programs'),
            ("announcements", "announcements")
        ]
    )
    number = serializers.IntegerField()


class GenerateData(APIView):
    @extend_schema(
        request=GenerateSerializer,
        responses={
            201: "Successfully generated data",
            400: "Invalid input",
        }
    )
    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        serializer = GenerateSerializer(data=request.data)
        if serializer.is_valid():
            model = serializer.validated_data['model']
            number = serializer.validated_data['number']

            factory_map = {
                'users': UserFactory,
                'instructors': InstructorFactory,
                'students': StudentFactory,
                'programs': ProgramFactory,
                'announcements': AnnouncementFactory
            }

            if model not in factory_map:
                return Response({"error": "Invalid model specified."}, status=400)

            if model == "programs":
                # Create programs
                created_programs = set([ProgramFactory()
                                       for _ in range(1, number)])

                created_courses = set()
                levels = ["beginner", "basic", "intermediate", "advanced"]

                for program in created_programs:

                    for l in range(int(program.duration)):
                        course = CourseFactory(program=program, name=f"{program.name}-{levels[l]}", level=l)
                        created_courses.add(course)

                return Response({
                    "message": f"{number} program objects and their courses have been created.",
                    "data": {
                        "programs": [program.pk for program in created_programs],
                        "courses": [course.pk for course in created_courses],
                    },
                }, status=201)

            # Special handling for instructors
            if model == "instructors":
                created_instructors = []
                programming_skills = [
                    "Python", "Excel", "Kotlin",
                    "Machine Learning", "Cybersecurity",
                    "Network Security", "Ethical Hacking", "Penetration Testing",
                    "React", "Javascript", "Vue", "Django", "Flutter"
                ]

                for _ in range(number):
                    instructor = InstructorFactory()
                    created_instructors.append(instructor)

                    num_skills = fake.random_int(min=1, max=5) 

                    skills = set([fake.random_element(elements=programming_skills) for _ in range(num_skills)])
                    for index, name in enumerate(skills):
                        try:
                            InstructorSkill.objects.get_or_create(
                                is_primary=(index == 0),  # First skill is primary
                                name=name
                            )
                        except IntegrityError:
                            # If the skill name is globally unique and already exists, skip or handle
                            print(f"Skill '{name}' already exists globally, skipping.")

                return Response({
                    "message": f"{number} instructor objects and their skills have been created.",
                    "data": {
                        "instructors": [instructor.pk for instructor in created_instructors],
                        "skills": [[skill.name for skill in instructor.skills.all()] for instructor in created_instructors],
                    },
                }, status=201)

            # Default behavior for other models
            factory = factory_map[model]
            created_objects = [factory() for _ in range(number)]

            return Response({
                "message": f"{number} {model} objects have been created.",
                "data": [obj.pk for obj in created_objects]
            }, status=201)

        return Response(serializer.errors, status=400)
