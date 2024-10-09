import pytest
from django.contrib.auth import get_user_model

pytestmark = pytest.mark.django_db


# def test_user_factory(user_factory):
#     user_factory.create()
#     assert get_user_model().objects.all().count() == 1


# def test_admin_user(admin_user):
#     assert admin_user.is_superuser == True

