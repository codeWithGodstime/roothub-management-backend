import pytest

from django.urls import reverse

from utils.strategies import CreateStrategy, UpdateStrategy, TestStrategyRunner
from utils.test_helper import TestHelper
from authentication import models
from course.models import Course

pytestmark = pytest.mark.django_db


class TestUserViewset:

    # def test_create_staff_user(self, api_client, admin_user):
    #     request_data = TestHelper().generate_test_data("user")
    #     api_client.force_authenticate(user=admin_user)

    #     unique = request_data['email']

    #     TestStrategyRunner.execute(
    #         CreateStrategy(
    #             api_client,
    #             reverse("users-list"),
    #             request_data,
    #             ['detail'],
    #             models.User,
    #             "email",
    #             unique
    #         )
    #     )

    #     qs = models.User.objects.get(email=unique)
    #     assert qs.is_staff

    # def test_create_instructor_user(self, api_client, admin_user):
    #     request_data = TestHelper().generate_test_data("instructor")
    #     api_client.force_authenticate(user=admin_user)

    #     unique = request_data['user']['email']

    #     TestStrategyRunner.execute(
    #         CreateStrategy(
    #             api_client,
    #             reverse("users-instructors"),
    #             request_data,
    #             ['detail'],
    #             models.User,
    #             "email",
    #             unique
    #         )
    #     )

    #     qs = models.User.objects.get(email=unique)
    #     assert qs.is_instructor

    # def test_create_student_user(self, api_client, admin_user, program_factory_fixture):

    #     program = program_factory_fixture()

    #     data_instance = TestHelper()
    #     request_data = data_instance.generate_test_data("student", program.id)
    #     unique = request_data['user']['email']

    #     api_client.force_authenticate(user=admin_user)

    #     TestStrategyRunner.execute(
    #         CreateStrategy(
    #             api_client,
    #             reverse("users-students"),
    #             request_data,
    #             ['detail'],
    #             models.User,
    #             "email",
    #             unique
    #         )
    #     )

    #     # check if user is student
    #     qs = models.User.objects.get(email=unique)
    #     assert qs.is_student

    def test_staff_can_create_student_account(self, api_client, user_factory_fixture, program_factory_fixture):
        user = user_factory_fixture.create(is_staff=True)
        program = program_factory_fixture()
        request_data = TestHelper().generate_test_data('student', program.id)
        api_client.force_authenticate(user=user)
        unique = request_data['user']['email']

        TestStrategyRunner.execute(
            CreateStrategy(
                api_client,
                reverse("users-students"),
                request_data,
                ['detail'],
                models.User,
                "email",
                unique
            )
        )
        qs = models.User.objects.get(email=unique)
        assert qs.is_student

    def test_student_is_added_to_course_on_registration(self, api_client, admin_user, program_factory_fixture, course_factory_fixture):
        program = program_factory_fixture(duration=3)
        course = course_factory_fixture(level=1, duration=1, name=f"{program.name}-basic", program=program)
        request_data = TestHelper().generate_test_data('student', program.id)
        api_client.force_authenticate(user=admin_user)
        unique = request_data['user']['email']

        TestStrategyRunner.execute(
            CreateStrategy(
                api_client,
                reverse("users-students"),
                request_data,
                ['detail'],
                models.User,
                "email",
                unique
            )
        )

        course.refresh_from_db()
      # Assert that the student is associated with the course
        course_students = course.students.all()
        assert len(course_students) == 1
        student = course_students.first()
        assert student.user.email == request_data['user']['email']




class TestProgram:
    def test_admin_can_create_programs(self, api_client, admin_user):
        api_client.force_authenticate(user=admin_user)
        request_data = TestHelper().generate_test_data('program')
        print(request_data, "REQUEST_DATA==")
        unique = request_data['name']

        TestStrategyRunner.execute(
            CreateStrategy(
                api_client,
                reverse("programs-list"),
                request_data,
                ["id", "name", "duration", "total_amount"],
                models.Program,
                "name",
                unique
            )
        )

        # check is courses is created
        # based on the duration check the number of course created 4- months basic, beginner, intermediate, advanced
        # 3 - beginner, intermediate, advanced  
        courses = Course.objects.all()
        assert len(courses) == request_data["duration"]

