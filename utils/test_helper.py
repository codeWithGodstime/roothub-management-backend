
import factory
import random

from django.db import models
from faker import Faker
from typing import Literal


faker = Faker()


class TestHelper:

    def student_data(self, program_id: str = None):
        return {
            "user": self.user_data(),
            "payment_plan": faker.random_choices(elements=['FULL', "PART", "NOT PAID"])[0],
            "type": faker.random_choices(elements=["INTERN", "EXTERN", "TRIPTERN"])[0],
            "program": program_id,
        }

    def instructor_data(self):
        return {
            "user": self.user_data()
        }

    def user_data(self):
        return {
            "email": faker.email(),
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "next_of_kin_name": faker.name(),
            "next_of_kin_contact": faker.basic_phone_number()[:11],
            "next_of_kin_email": faker.email(),
            "next_of_kin_relationship": faker.random_choices(elements=["SISTER", "BROTHER", "FATHER", "SON", "DAUGHTER", "COLLEAGUE"])[0],
            "home_address": faker.address()
        }

    def program_data(self):
        return {
            "name": faker.random_choices(elements=["web development", 'python', 'data analysis', 'graphics design'])[0],
            "total_amount": faker.pydecimal(left_digits=7, min_value=50000, right_digits=2),
            "duration": faker.random_choices(elements=[x for x in range(1, 4)])[0]
        }

    def course_data(self, program: models.Model, instructor: models.Model):
        levels = {
            "Beginner": 1,
            "Basic": 2,
            "Intermediate": 3,
            "Advanced": 4,
        }
        level_name = random.choice(list(levels.keys()))  # Randomly select a course level
        return {
            "name": f"{program.name}-{level_name.lower()}",
            "program": program.id,
            "instructor": instructor.id,
            "level": levels[level_name],  # Map level name to its numeric value
            "duration": 4,  # Example duration
        }

    def generate_test_data(self, type: Literal["user", "instructor", "student", 'program', "course"], *args):

        if type == 'student' and args:

            program_id = args[0]
            return self.student_data(program_id=program_id)

        if type == "course" and args:
            program = args[0]
            instructor = args[1]
            return self.course_data(program=program, instructor=instructor)

        data_dict = {
            "user": self.user_data(),
            "instructor": self.instructor_data(),
            "program": self.program_data()
        }

        return data_dict[type]


def compare_dict_data(received: dict, expected: list):
    """
    Compares the values of two dictionaries for matching keys.

    Args:
        received (dict): The actual dictionary received.
        expected (dict): The expected dictionary to compare against.

    Returns:
        tuple: A boolean indicating success, and a message detailing mismatched values if any.
    """
    results = []
    for value in expected:
        if value in received.keys():
            results.append(True)
        else:
            results.append(False)
    return all(results)
