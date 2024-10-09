from collections.abc import Callable
from typing import Any

import pytest
from faker import Faker

from django.conf import settings
from rest_framework.test import APIClient


faker = Faker()

@pytest.fixture()
def api_client():
    return APIClient()

@pytest.fixture()
def data():
    return {
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "password": faker.password(),
        "email": faker.email()
    }

@pytest.fixture
def has_fields() -> Callable[[dict[str, Any], list[str]], bool]:
    return lambda data, fields: all([x in data for x in fields])

@pytest.fixture(scope='session', autouse=True)
def configure_django_settings():
    settings.SECURE_SSL_REDIRECT = False