import pytest


from authentication.tests.factories import user_factory, program_factory, student_factory, instruction_factory
from course.tests.factories import course_factory


from rest_framework.test import APIClient

@pytest.fixture()
def api_client() -> APIClient:
    return APIClient()

@pytest.fixture
def user_factory_fixture() -> user_factory.UserFactory:
    return user_factory.UserFactory

@pytest.fixture
def program_factory_fixture() -> program_factory.ProgramFactory:
    return program_factory.ProgramFactory

@pytest.fixture
def student_factory_fixture() -> student_factory.StudentFactory:
    return student_factory.StudentFactory

@pytest.fixture
def instructor_fixture() -> instruction_factory.InstructorFactory:
    return instruction_factory.InstructorFactory

@pytest.fixture
def course_factory_fixture() -> course_factory.CourseFactory:
    return course_factory.CourseFactory