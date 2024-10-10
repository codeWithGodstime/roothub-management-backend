from collections.abc import Callable
from typing import Any, Literal

import pytest
from pytest_factoryboy import register
from faker import Faker

from django.conf import settings
from rest_framework.test import APIClient
from utils.test_helper import TestHelper
from course.tests.course_factories import CourseFactory

faker = Faker()
test_helper = TestHelper() # get test data for api endpoint

@pytest.fixture()
def api_client():
    return APIClient()

@pytest.fixture()
def test_data() -> TestHelper:
    return test_helper

@pytest.fixture
def has_fields() -> Callable[[dict[str, Any], list[str]], bool]:
    return lambda data, fields: all([x in data for x in fields])

register(CourseFactory)