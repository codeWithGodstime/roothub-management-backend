# import pytest
# from django.urls import reverse
# from django.contrib.auth import get_user_model
# from faker import Faker

# from authentication.models import Student, Instructor
# from course.models import CourseSession

# pytestmark = [pytest.mark.django_db, pytest.mark.apiTest]
# faker = Faker()


# def test_register_user(api_client, admin_user, test_data):

#     data = test_data.generate_test_data("user")
#     # authenticate as admin user
#     api_client.force_authenticate(user=admin_user)

#     url = reverse("users-list")
#     # check url part
#     assert url == "/v1/users/"

#     response = api_client.post(url, data, format='json')

#     assert response.status_code == 201
#     assert response.data['detail'] == f"User registration is successful, user credentials has been sent to {data['email']}"

# def test_register_student(api_client, admin_user, course_factory, test_data):
#     course = course_factory.create()

#     data = test_data.generate_test_data("student", {'course_id': course.id})
#     api_client.force_authenticate(user=admin_user)

#     url = reverse("users-students")

#     # check url part
#     assert url == "/v1/users/students/"

#     response = api_client.post(url, data, format='json')

#     assert response.status_code == 201
#     assert response.data['detail'] == f"Student registration is successful, user credentials has been sent to {data["user"]['email']}"
#     get_user_model().objects.get(email=data["user"]['email']).refresh_from_db()
#     user = get_user_model().objects.get(email=data["user"]['email'])
#     assert user.is_student
#     assert not user.is_instructor
#     assert not user.is_superuser
#     assert not user.is_staff

#     # check if student model exist
#     student_count = Student.objects.all().count()

#     assert student_count == 1
#     course_session_count = CourseSession.objects.all().count()
#     assert course_session_count == 1

# def test_register_instructor(api_client, admin_user, test_data):
#     data = test_data.generate_test_data("instructor")
#     api_client.force_authenticate(user=admin_user)

#     url = reverse("users-instructors")

#     # check url part
#     assert url == "/v1/users/instructors/"

#     response = api_client.post(url, data, format='json')

#     assert response.status_code == 201
#     assert response.data['detail'] == f"Instructor registration is successful, user credentials has been sent to {data["user"]['email']}"
#     get_user_model().objects.get(email=data["user"]['email']).refresh_from_db()
#     staff = get_user_model().objects.get(email=data["user"]['email'])
#     assert staff.is_instructor
#     assert not staff.is_staff
#     assert not staff.is_superuser
#     assert not staff.is_student

#     instructor_count = Instructor.objects.all().count()

#     assert instructor_count == 1

# def test_get_all_users(api_client, admin_user, user_factory):
#     user_factory.create_batch(10)
#     api_client.force_authenticate(user=admin_user)

#     url = reverse("users-list")

#     response = api_client.get(url, format='json')

#     assert response.status_code == 200
#     assert len(response.data['results']) == 11
#     # assert has_fields(
#     #                 response.data.get("results")[0]
#     #                 if response_data.get("count")
#     #                 else {},
#     #                 required_fields,
#     #             )

# def test_get_users_not_admin(api_client, instructor_user, user_factory):
#     user_factory.create_batch(10)
#     api_client.force_authenticate(user=instructor_user)

#     url = reverse("users-list")

#     response = api_client.get(url, format='json')

#     assert response.status_code == 403
