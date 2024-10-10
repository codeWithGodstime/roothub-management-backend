import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from faker import Faker

pytestmark = [pytest.mark.django_db, pytest.mark.course, pytest.mark.apiTest]
faker = Faker()


def test_admin_can_create_course(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    url = reverse("courses-list")
    assert url == "/v1/courses/"

    data = {
    "name": "Web development",
    "total_amount": "619552.65",
    "duration": "3"
    }

    response = api_client.post(url, data, format="json")
    assert response.status_code == 201

    assert all(field in list(response.data.keys()) for field in ["name", "total_amount", "duration", "student_count", "instructors"])
