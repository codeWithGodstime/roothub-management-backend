import pytest

from django.urls import reverse

from utils.strategies import CreateStrategy, UpdateStrategy, ListStrategy, NotPermittedGetStrategy, TestStrategyRunner
from utils.test_helper import TestHelper
from authentication import models
from course.models import Course, CourseSession

pytestmark = pytest.mark.django_db


class TestUserViewsetCreation:

    def test_create_staff_user(self, api_client, admin_user):
        request_data = TestHelper().generate_test_data("user")
        api_client.force_authenticate(user=admin_user)

        unique = request_data['email']

        TestStrategyRunner.execute(
            CreateStrategy(
                api_client,
                reverse("users-list"),
                request_data,
                ['detail'],
                models.User,
                "email",
                unique
            )
        )

        qs = models.User.objects.get(email=unique)
        assert qs.is_staff

    def test_create_instructor_user(self, api_client, admin_user):
        request_data = TestHelper().generate_test_data("instructor")
        api_client.force_authenticate(user=admin_user)

        unique = request_data['user']['email']

        TestStrategyRunner.execute(
            CreateStrategy(
                api_client,
                reverse("users-instructors"),
                request_data,
                ['detail'],
                models.User,
                "email",
                unique
            )
        )

        qs = models.User.objects.get(email=unique)
        assert qs.is_instructor

    def test_admin_can_get_all_instructors(self, api_client, admin_user, instructor_fixture):
        api_client.force_authenticate(user=admin_user)
        instructors = instructor_fixture.create_batch(20)

        TestStrategyRunner.execute(
            ListStrategy(
                api_client,
                reverse("instructors-list"),
                models.Instructor,
                ["id", "fullname", "number_of_active_trainees",
                    "sessions", "payment_due", "expertise"],
                20
            )
        )

    def test_create_student_user(self, api_client, admin_user, program_factory_fixture):

        program = program_factory_fixture()

        data_instance = TestHelper()
        request_data = data_instance.generate_test_data("student", program.id)
        unique = request_data['user']['email']

        api_client.force_authenticate(user=admin_user)

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

        # check if user is student
        qs = models.User.objects.get(email=unique)
        assert qs.is_student

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
        course = course_factory_fixture(level=1, duration=1, name=f"{
                                        program.name}-basic", program=program)
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


class TestAccounts:
    def test_forget_password_valid_email(self, api_client, user_factory_fixture):
        user = user_factory_fixture()

        payload = {"email": user.email}
        response = api_client.post(reverse('users-reset-password'), payload)
        assert response.status_code == 200
        assert response.data["message"] == "We have sent you a link to reset your password"

    def test_forget_password_invalid_email(self, api_client):
        payload = {"email": "test@gmail.com"}
        response = api_client.post(reverse('users-reset-password'), payload)

        assert response.status_code == 404
        assert response.data["error"] == "User with email not found"

    def test_forget_password_missing_email(self, api_client):
        payload = {}
        response = api_client.post(reverse('users-reset-password'), payload)

        assert response.status_code == 400
        assert "email" in response.data

    def test_change_password_success(self, api_client, generate_reset_token):

        url = reverse("users-change-password")
        new_password = "NewSecurePassword123!"
        user, token = generate_reset_token

        response = api_client.post(
            url,
            data={"token": f"{user.id}:{token}", "new_password": new_password},
            format="json",
        )

        assert response.status_code == 200
        assert response.data["message"] == "Password updated successfully."

        # Verify the password has been updated
        user.refresh_from_db()
        assert user.check_password(new_password)

    def test_change_password_invalid_token(self, api_client):
        url = reverse("users-change-password")
        invalid_token = "1:InvalidToken123"
        new_password = "NewSecurePassword123!"

        response = api_client.post(
            url,
            data={"token": invalid_token, "new_password": new_password},
            format="json",
        )

        assert response.status_code == 400
        assert "token" in response.data

    def test_change_password_missing_token(self, api_client):
        url = reverse("users-change-password")
        new_password = "NewSecurePassword123!"

        response = api_client.post(
            url,
            data={"new_password": new_password},
            format="json",
        )

        assert response.status_code == 400
        assert "token" in response.data

    def test_change_password_password_validation_failure(self, api_client, generate_reset_token):
        url = reverse("users-change-password")
        weak_password = "123"
        user, token = generate_reset_token

        response = api_client.post(
            url,
            data={"token": token, "new_password": weak_password},
            format="json",
        )

        assert response.status_code == 400
        assert "new_password" in response.data


class TestProgram:
    def test_admin_can_create_programs(self, api_client, admin_user):
        api_client.force_authenticate(user=admin_user)
        request_data = TestHelper().generate_test_data('program')
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


class TestStudent:
    def test_list_student_endpoint(self, api_client, admin_user, student_factory_fixture):
        students = student_factory_fixture.create_batch(10)

        api_client.force_authenticate(user=admin_user)

        TestStrategyRunner.execute(
            ListStrategy(
                api_client,
                reverse("students-list"),
                model=models.Student,
                expected_data=[
                    "id",
                    "user",
                    "program",
                    "tutor",
                    "level",
                    "balance",
                    "amount_paid",
                    "type"
                ],
                count=10
            )
        )


class TestInstructor:
    def test_instructor_can_see_all_his_active_sessions(self, api_client, instructor_fixture, program_with_course_fixture):
        instructor = instructor_fixture()
        prog = program_with_course_fixture(instructor)

        api_client.force_authenticate(user=instructor.user)

        TestStrategyRunner.execute(
            ListStrategy(
                api_client,
                reverse("instructors-active-sessions", args=[instructor.id]),
                CourseSession,
                ["id", "start_date", "estimated_end_date",
                    "end_date", "course", "created_at", "is_active"],
                1
            )
        )

    def test_instructor_cannot_see_another_instructor_sessions(self, api_client, instructor_fixture, program_with_course_fixture):
        owner_instructor = instructor_fixture()
        program_with_course_fixture = program_with_course_fixture(
            owner_instructor)

        instructor = instructor_fixture()
        api_client.force_authenticate(user=instructor.user)

        TestStrategyRunner.execute(
            NotPermittedGetStrategy(
                api_client,
                reverse("instructors-active-sessions",
                        args=[owner_instructor.id]),
                None,
                403
            )
        )
