import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from faker import Faker


pytestmark = [pytest.mark.django_db, pytest.mark.authTest]


class TestAuthenticationEndpoint:

    def test_admin_can_create_staff_account(self, api_client, admin_user, test_data):
        data = test_data.generate_test_data("staff")

        api_client.force_authenticate(user=admin_user)
        url = reverse("users-list")
        assert url == "/v1/users/"
        response = api_client.post(url, data, format="json")
        assert response.status_code == 201
        assert response.data['detail'] ==  f"User registration is successful, user credentials has been sent to {data['email']}"

        user = get_user_model().objects.get(email=data['email'])
        assert user.is_staff
    
    def test_not_admin_can_create_staff_account(self, api_client, staff_user, test_data):
        data = test_data.generate_test_data("staff")

        api_client.force_authenticate(user=staff_user)
        url = reverse("users-list")
        assert url == "/v1/users/"
        response = api_client.post(url, data, format="json")
        assert response.status_code == 403

    def test_admin_can_create_program(self, api_client, admin_user, test_data):
        data = test_data.generate_test_data("program")

        api_client.force_authenticate(user=admin_user)
        url = reverse("programs-list")
        assert url == "/v1/programs/"
        response = api_client.post(url, data, format="json")

        assert response.status_code == 201
        print(data)
        assert test_data.compare_dict_data(response.data, data)


    # def test_admin_create_student_account(self, api_client, admin_user, test_data):
    #     data = test_data.generate_test_data("student")

    #     api_client.force_authenticate(user=admin_user)

    #     url = reverse("users-students")
    #     assert url == "/v1/users/students/"

    #     response = api_client.post(url, data, format="json")

    #     assert response.status_code == 201
    #     assert response.data['detail'] == f"User registration is successful, user credentials has been sent to {data['email']}"

    #     # check is the is_student fieldi is true
    #     user = get_user_model().objects.get(email=data['email'])
    #     assert user.is_student
    
    # def test_staff_can_create_student_account(self, api_client, staff_user, test_data):
    #     data = test_data.generate_test_data("staff")

    #     api_client.force_authenticate(user=staff_user)

    #     url = reverse("users-students")
    #     assert url == "/v1/users/students/"

    #     response = api_client.post(url, data, format="json")
    #     print(response.data, response.status_code)
    #     assert response.status_code == 201
    #     assert response.data['detail'] == f"User registration is successful, user credentials has been sent to {data['email']}"

    #     user = get_user_model().objects.get(email=data['email'])
    #     assert user.is_student

    # def test_normal_user_can_create_account(self, api_client, user, test_data):
    #     data = test_data.generate_test_data("user")
    #     api_client.force_authenticate(user=user)

    #     url = reverse("users-list")
    #     assert url == "/v1/users/"

    #     response = api_client.post(url, data, format="json")

    #     assert response.status_code == 403
    #     assert "You do not have permission to perform this action" in response.data['detail']

    #     user = get_user_model().objects.get(email=data['email'])
    #     assert user.is_staff
    
    # def test_admin_can_create_instructor_account(self, api_client, instructor_user, test_data):
    #     assert False
    
    # def test_admin_create_instructor_account(self, api_client, admin_user, test_data):
    #     data = test_data.generate_test_data("instructor")

    #     api_client.force_authenticate(user=admin_user)
    #     url = reverse("users-list")
    #     assert url == "/v1/users/"

    #     response = api_client.post(url, data, format="json")
    #     assert response.status_code == 201
