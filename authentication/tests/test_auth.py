# import pytest

# from django.urls import reverse

# from utils.strategies import CreateStrategy, UpdateStrategy, TestStrategyRunner
# from utils.test_helper import TestHelper
# from authentication import models

# pytestmark = pytest.mark.django_db

# class TestUserViewset:

#     def test_create_staff_user(self, api_client, admin_user):
#         request_data = TestHelper().generate_test_data("user")
#         api_client.force_authenticate(user=admin_user)

#         unique = request_data['email']

#         TestStrategyRunner.execute(
#             CreateStrategy(
#                 api_client,
#                 reverse("users-list"),
#                 request_data,
#                 ['detail'],
#                 models.User,
#                 "email",
#                 unique
#             )
#         )

#         qs = models.User.objects.get(email=unique)
#         assert qs.is_staff


#     def test_create_instructor_user(self, api_client, admin_user):
#         request_data = TestHelper().generate_test_data("instructor")
#         api_client.force_authenticate(user=admin_user)

#         unique = request_data['user']['email']

#         TestStrategyRunner.execute(
#             CreateStrategy(
#                 api_client,
#                 reverse("users-instructors"),
#                 request_data,
#                 ['detail'],
#                 models.User,
#                 "email",
#                 unique
#             )
#         )

#         qs = models.User.objects.get(email=unique)
#         assert qs.is_instructor

#     def test_create_student_user(self, api_client, admin_user, program_factory_fixture):

#         program = program_factory_fixture()

#         data_instance = TestHelper()
#         request_data = data_instance.generate_test_data("student", program.id)
#         unique = request_data['user']['email']

#         api_client.force_authenticate(user=admin_user)

#         TestStrategyRunner.execute(
#             CreateStrategy(
#                 api_client,
#                 reverse("users-students"),
#                 request_data,
#                 ['detail'],
#                 models.User,
#                 "email",
#                 unique
#             )
#         )

#         # check if user is student
#         qs = models.User.objects.get(email=unique)
#         assert qs.is_student

#     def test_staff_can_create_student_account(self, api_client, user_factory_fixture, program_factory_fixture):
#         user = user_factory_fixture.create(is_staff=True)
#         program = program_factory_fixture()
#         request_data = TestHelper().generate_test_data('student', program.id)
#         api_client.force_authenticate(user=user)
#         unique = request_data['user']['email']

#         TestStrategyRunner.execute(
#             CreateStrategy(
#                 api_client,
#                 reverse("users-students"),
#                 request_data,
#                 ['detail'],
#                 models.User,
#                 "email",
#                 unique
#             )
#         )
#         qs = models.User.objects.get(email=unique)
#         assert qs.is_student


# class TestProgram:
#     def test_admin_can_create_programs(self, api_client, admin_user):
#         api_client.force_authenticate(user=admin_user)
#         request_data = TestHelper().generate_test_data('program')
#         unique = request_data['name']

#         TestStrategyRunner.execute(
#             CreateStrategy(
#                 api_client,
#                 reverse("programs-list"),
#                 request_data,
#                 ['detail'],
#                 models.Program,
#                 "name",
#                 unique
#             )
#         )