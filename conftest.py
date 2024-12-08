from collections.abc import Callable
from typing import Any, Literal

import pytest
from pytest_factoryboy import register
from faker import Faker

from django.conf import settings
from rest_framework.test import APIClient
from utils.test_helper import TestHelper
from authentication.tests.auth_factories import UserFactory, ProgramFactory#, StudentPresentation, StudentPresentationFactory, InstructorFactory, StudentFactory
# from course.tests.course_factories import CourseFactory

faker = Faker()
test_helper = TestHelper() # get test data for api endpoint

@pytest.fixture()
def api_client():
    return APIClient()

@pytest.fixture()
def test_data() -> TestHelper:
    return test_helper


# register(CourseFactory)
register(UserFactory)
register(ProgramFactory)
# register(StudentPresentationFactory)
# register(StudentFactory)
# register(InstructorFactory)


@pytest.fixture()
def admin_user(user_factory):
    admin = user_factory.create(is_superuser=True, is_staff=True, email='admin@gmail.com')
    return admin

@pytest.fixture()
def staff_user(user_factory):
    staff = user_factory.create(is_superuser=False, is_staff=True, email='staff@gmail.com')
    return staff

@pytest.fixture()
def student_user(user_factory):
    user = user_factory.create(is_student=True)
    return user

@pytest.fixture()
def instructor_user(user_factory):
    user = user_factory.create(is_instructor=True)
    return user

@pytest.fixture()
def test_program(program_factory):
    program = program_factory.create()
    return program