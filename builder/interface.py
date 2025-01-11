from abc import ABC, abstractmethod
from rest_framework.test import APIClient
from django.urls import reverse


class Builder(ABC):
    def __init__(self):
        super().__init__()
        self.client = APIClient()

    @abstractmethod
    def login(self):
        pass

    @abstractmethod
    def register_user(self):
        pass

    @abstractmethod
    def reset_password(self):
        pass

    @abstractmethod
    def forget_password(self):
        pass

    @abstractmethod
    def change_password(self):
        pass

    @abstractmethod
    def get_profile(self):
        pass


class UserBuilder(Builder):
    """
        UserBuilder contains implementations for actions that can be performed by different users with various
    """

    def login(self, data: dict):
        url = reverse("token")
        response = self.client.post(url, data, format="json")
        assert response.status_code == 201
        assert all(field in ["access", "refresh", "user"] for field in response.data.keys())
        
    def register_user(self, data: dict):
        pass

    def reset_password(self, data: dict):
        pass

    def forget_password(self, data:dict):
        pass

    def change_password(self, data:dict):
        pass

    def get_profile(self, user):
        pass

u = UserBuilder()
data = {
  "email": "admin2@gmail.com",
  "user_type_info": "",
  "first_name": "<string>",
  "last_name": "<string>"
}
u.login({"email": "admin@gmail.com", "password": ""})
