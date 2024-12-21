import pytest

from django.urls import reverse

from utils.strategies import CreateStrategy, UpdateStrategy
from utils.test_helper import TestHelper, TestStrategyRunner
from authentication import models


class TestUserViewset:

    def test_create_staff_user(self, api_client, user_factory_fixture, admin_user):
        request_data = TestHelper.get_data(user_factory_fixture)
        api_client.force_authenticate(user=admin_user)

        TestStrategyRunner.execute(
            CreateStrategy(
                api_client, 
                reverse("users-list"), 
                request_data, 
                ['detail'], 
                models.User, 
                "email"
                )
            )

    
    def test_update_user(self, api_client, user_factory_fixture, admin_user):
        # create user
        user = user_factory_fixture()

        request_data = TestHelper.get_data(user_factory_fixture)
        
        api_client.force_authenticate(user=admin_user)

        TestStrategyRunner.execute(
            UpdateStrategy(
                api_client, 
                reverse("users-detail", args=[user.id]), 
                request_data,
                [],
                models.User, 
                user.id
            )
        )

