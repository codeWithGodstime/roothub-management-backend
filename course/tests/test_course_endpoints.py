# import pytest
# from django.urls import reverse
# from django.contrib.auth import get_user_model
# from faker import Faker

# pytestmark = [pytest.mark.django_db, pytest.mark.course, pytest.mark.apiTest]
# faker = Faker()


# def test_admin_can_create_course(api_client, admin_user, test_data):
#     data = test_data.generate_test_data('course')
#     api_client.force_authenticate(user=admin_user)
#     url = reverse("courses-list")
#     assert url == "/v1/courses/"

#     response = api_client.post(url, data, format="json")

#     assert response.status_code == 201

#     assert all(field in list(response.data.keys()) for field in ["name", "total_amount", "duration", "student_count", "instructors", "monthly_amount", "active_sessions"])

# def test_get_unassigned_course_sessions(api_client, admin_user, student_factory):
#     api_client.force_authenticate(user=admin_user)

#     student_factory.create_batch(5)
#     url = reverse("sessions-list")
#     assert url == "/v1/sessions/"

#     response = api_client.get(url, format="json")
#     assert response.status_code == 200
#     assert len(response.data["results"]) == 5

# # TODO: test add student for course with sessions instructors



