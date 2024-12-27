import pytest

from django.urls import reverse
from announcement.models import Announcement

from utils.strategies import CreateStrategy, UpdateStrategy, TestStrategyRunner, NotPermittedStrategy
from utils.test_helper import TestHelper

pytestmark = pytest.mark.django_db


class TestAnnouncement:

    def test_admin_can_create_announcement(self, api_client, admin_user):
        request_data = TestHelper().generate_test_data("announcement")
        unique = request_data['title']

        api_client.force_authenticate(user=admin_user)

        TestStrategyRunner.execute(
            CreateStrategy(
                api_client,
                reverse("announcements-list"),
                request_data,
                ["id", "title", "message", "schedule_date", "schedule_time", "receiver_group", "created_at", "updated_at"],
                Announcement,
                "title",
                unique
            )
        )

    def test_non_admin_can_create_announcement(self, api_client, user_factory_fixture):
        student = user_factory_fixture.create(is_student=True)
        request_data = TestHelper().generate_test_data("announcement")

        api_client.force_authenticate(user=student)

        TestStrategyRunner.execute(
            NotPermittedStrategy(
                api_client,
                reverse("announcements-list"),
                request_data,
                expected_status_code=403
            )
        )

        # check for staff
        staff = user_factory_fixture.create(is_staff=True)
        request_data = TestHelper().generate_test_data("announcement")

        api_client.force_authenticate(user=staff)

        TestStrategyRunner.execute(
            NotPermittedStrategy(
                api_client,
                reverse("announcements-list"),
                request_data,
                expected_status_code=403
            )
        )

    def test_admin_update_announcement(self, api_client, admin_user, announcement_factory_fixture):
        announcement = announcement_factory_fixture()
        api_client.force_authenticate(user=admin_user)
        request_data = TestHelper().generate_test_data("announcement")

        TestStrategyRunner.execute(
            UpdateStrategy(
                api_client,
                reverse("announcements-detail", args=[announcement.id]),
                request_data,
                ["id", "title", "message", "schedule_date", "schedule_time", "receiver_group", "created_at", "updated_at"],
                Announcement,
                "id",
                announcement.id,
                "full"
            )
        )



