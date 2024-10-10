import pytest
from decimal import Decimal
from django.urls import reverse
from django.contrib.auth import get_user_model
from faker import Faker

pytestmark = [pytest.mark.django_db, pytest.mark.course, pytest.mark.apiTest]
faker = Faker()

def test_course_model(course_factory):
# Create a course instance using the factory
    course = course_factory.create(
        name="Web Development",
        total_amount=Decimal('150000.00'),
        duration="3"
    )

    # Assert that the course name is correctly set
    assert course.name == "Web Development"
    
    # Assert that the total amount is correctly set
    assert course.total_amount == Decimal('150000.00')

    # Calculate the expected monthly amount manually
    expected_monthly_amount = Decimal('150000.00') / 3
    
    # Assert that the monthly amount is correctly calculated
    assert course.monthly_amount == expected_monthly_amount