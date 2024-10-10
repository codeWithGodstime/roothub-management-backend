import pytest
from pytest_factoryboy import register

from .auth_factories import UserFactory, StudentPresentationFactory, StudentFactory, InstructorFactory

pytestmark = pytest.mark.django_db

register(UserFactory)
register(StudentPresentationFactory)
register(StudentFactory)
register(InstructorFactory)


@pytest.fixture()
def admin_user(user_factory):
    admin = user_factory.create(is_superuser=True, is_staff=True, email='admin@gmail.com')
    return admin

@pytest.fixture()
def student_user(user_factory):
    user = user_factory.create(is_student=True)
    return user

@pytest.fixture()
def instructor_user(user_factory):
    user = user_factory.create(is_instructor=True)
    return user