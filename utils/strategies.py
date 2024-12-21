from abc import abstractmethod, ABC
from rest_framework.test import APIClient
from django.db import models


class TestStrategy(ABC):

    def __init__(self, client: APIClient, url: str, data: dict, expected_data: list):
        self.client = client
        self.url = url
        self.data = data
        self.expected_data = expected_data

    @abstractmethod
    def act(self):
        pass

    @abstractmethod
    def assert_(self, expected_response: dict):
        pass


class CreateStrategy(TestStrategy):

    def __init__(self, client: APIClient, url: str, data: dict, expected_data: list, model: models.Model, unique_field: str):
        super().__init__(client, url, data, expected_data)
        self.model = model
        self.unique_field = unique_field

    def act(self):
        self.response = self.client.post(self.url, self.data, format='json')
    
    def assert_(self):
        assert self.response.status_code == 201
        qs = self.model.objects.filter(
            email=self.data.get(self.unique_field)).exists()
        assert qs


class UpdateStrategy(TestStrategy):
    def __init__(self, client: APIClient, url: str, data: dict, expected_data: list, model: models.Model, unique_field: str):
        super().__init__(client, url, data, expected_data)
        self.model = model
        self.unique_field = unique_field

    def act(self):
        self.response = self.client.put(self.url, self.data, format='json')  # For a full update

    def assert_(self):
        # Check for successful response
        assert self.response.status_code in (200, 202), f"Unexpected status code: {self.response.status_code}"
        
        # Ensure the data in the response matches expected data
        results = []
        for value in self.expected_data:
            if value in self.response.data.keys():
                results.append(True)
            else:
                results.append(False)
        assert all(results)

        # Validate that the changes are reflected in the database
        instance = self.model.objects.filter(id=self.unique_field).first()
        assert instance is not None, "Updated instance not found in the database"


class DeleteStrategy(TestStrategy):
    def __init__(self, client: APIClient, url: str, model: models.Model, unique_field: str, unique_value: str):
        super().__init__(client, url, {}, [])
        self.model = model
        self.unique_field = unique_field
        self.unique_value = unique_value

    def act(self):
        self.response = self.client.delete(self.url, format='json')

    def assert_(self):
        # Check the response status code
        assert self.response.status_code in (204, 202), f"Unexpected status code: {self.response.status_code}"
        
        # Validate that the object is deleted in the database
        exists = self.model.objects.filter(**{self.unique_field: self.unique_value}).exists()
        assert not exists, f"Object with {self.unique_field}={self.unique_value} still exists in the database"

class ListStrategy(TestStrategy):
    def __init__(self, client: APIClient, url: str, expected_data: list):
        super().__init__(client, url, {}, expected_data)

    def act(self):
        self.response = self.client.get(self.url, format='json')

    def assert_(self):
        # Check the response status code
        assert self.response.status_code == 200, f"Unexpected status code: {self.response.status_code}"
        
        # Validate the response data
        response_data = self.response.data
        assert isinstance(response_data, list), "Expected response data to be a list"
        assert len(response_data) == len(self.expected_data), (
            f"Expected {len(self.expected_data)} items, but got {len(response_data)}"
        )
        
        for expected_item in self.expected_data:
            assert expected_item in response_data, f"Missing item: {expected_item}"
