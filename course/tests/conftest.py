import pytest
from pytest_factoryboy import register

from .course_factories import CourseFactory

pytestmark = pytest.mark.django_db

register(CourseFactory)