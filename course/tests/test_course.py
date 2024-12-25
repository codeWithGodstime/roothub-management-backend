import pytest

from django.urls import reverse

# from authentication.tests.factories import program_factory
from utils.strategies import CreateStrategy, UpdateStrategy, TestStrategyRunner
from utils.test_helper import TestHelper
from course import models

pytestmark = pytest.mark.django_db


class TestCourse:
    def test_admin_can_create_programs(self, api_client, admin_user, program_factory_fixture, instructor_fixture):

        program = program_factory_fixture()
        instructor = instructor_fixture()

        api_client.force_authenticate(user=admin_user)
        request_data = TestHelper().generate_test_data('course', program, instructor)
        unique = request_data['name']

        TestStrategyRunner.execute(
            CreateStrategy(
                api_client,
                reverse("courses-list"),
                request_data,
                ['id', "name", "program", "instructor", "duration", "level"],
                models.Course,
                "name",
                unique
            )
        )

    def test_admin_can_assign_instructor_to_course(self, api_client, admin_user, program_with_course_fixture, instructor_fixture):
        program, course = program_with_course_fixture()
        instructor = instructor_fixture()

        api_client.force_authenticate(user=admin_user)

        response = api_client.post(
            reverse("courses-assign", args=[course.id]), 
            {"instructor_id": instructor.id},
            format="json"
        )
        
        assert response.status_code == 200
        # Ensure the data in the response matches expected data
        results = []
        for value in ["id", "name", "program", "duration", "instructor", "level"]:
            if value in response.data.keys():
                results.append(True)
            else:
                results.append(False)
        assert all(results)
        assert response.data['instructor'] == instructor.id


class TestCourseSession:
    def test_instructor_can_add_student_to_course_session(self, api_client, instructor_fixture, course_with_instructor_fixture, program_factory_fixture, student_factory_fixture, course_session_fixture):
        instructor = instructor_fixture()
        program = program_factory_fixture()
        course = course_with_instructor_fixture.create(instructor=instructor, program=program)
        course_session = course_session_fixture.create(course=course)
        print(course_session, "course_session===", course_session.id)
        student = student_factory_fixture()
        print(instructor.user)
        api_client.force_authenticate(user=instructor.user)

        response = api_client.post(
            reverse("sessions-add", args=[course_session.id]),
            {
                "student_id": student.id,
            }
        )
        print(response.data)
        assert response.status_code == 200
