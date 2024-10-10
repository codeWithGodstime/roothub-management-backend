import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from faker import Faker

pytestmark = [pytest.mark.django_db, pytest.mark.apiTest]
faker = Faker()


def test_register(api_client, admin_user, data):
    # authenticate as admin user
    api_client.force_authenticate(user=admin_user)

    url = reverse("users-list")
    # check url part
    assert url == "/v1/users/"

    response = api_client.post(url, data, format='json')

    assert response.status_code == 201
    assert response.data['detail'] == f"User registration is successful, user credentials has been sent to {data['email']}"

def test_register_student(api_client, admin_user, data):
    api_client.force_authenticate(user=admin_user)

    url = reverse("users-students")

    # check url part
    assert url == "/v1/users/students/"

    response = api_client.post(url, data, format='json')

    assert response.status_code == 201
    assert response.data['detail'] == f"Student registration is successful, user credentials has been sent to {data['email']}"
    get_user_model().objects.get(email=data["email"]).refresh_from_db()
    student = get_user_model().objects.get(email=data['email'])
    assert student.is_student
    assert not student.is_instructor
    assert not student.is_superuser
    assert not student.is_staff

def test_register_instructor(api_client, admin_user, data):
    api_client.force_authenticate(user=admin_user)

    url = reverse("users-instructors")

    # check url part
    assert url == "/v1/users/instructors/"

    response = api_client.post(url, data, format='json')

    assert response.status_code == 201
    assert response.data['detail'] == f"Instructor registration is successful, user credentials has been sent to {data['email']}"
    get_user_model().objects.get(email=data['email']).refresh_from_db()
    staff = get_user_model().objects.get(email=data['email'])
    assert staff.is_instructor
    assert not staff.is_staff
    assert not staff.is_superuser
    assert not staff.is_student

def test_get_all_users(api_client, admin_user, user_factory, has_fields):
    user_factory.create_batch(10)
    api_client.force_authenticate(user=admin_user)

    url = reverse("users-list")

    response = api_client.get(url, format='json')

    assert response.status_code == 200
    assert len(response.data['results']) == 11
    # assert has_fields(
    #                 response.data.get("results")[0]
    #                 if response_data.get("count")
    #                 else {},
    #                 required_fields,
    #             )

def test_get_users_not_admin(api_client, instructor_user, user_factory, has_fields):
    user_factory.create_batch(10)
    api_client.force_authenticate(user=instructor_user)

    url = reverse("users-list")

    response = api_client.get(url, format='json')

    assert response.status_code == 403
