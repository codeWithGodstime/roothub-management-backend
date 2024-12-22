
import factory
from faker import Faker
from typing import Literal

from .strategies import TestStrategy

faker = Faker()

class TestHelper:

    def student_data(self, program_id:str = None):
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

    def generate_test_data(self, type: Literal["user", "instructor", "student", 'program'], *args, **kwargs):
        if type == 'student' and args:
            program_id = args[0]
            return self.student_data(program_id=program_id)
        
        data_dict = {
            "user": self.user_data(),
            "instructor": self.instructor_data(),
            "program": self.program_data()
        }

        return data_dict[type]

    @staticmethod
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


class TestStrategyRunner:
    """
    A class responsible for executing a given test strategy.

    This class defines a method `execute`, which takes a `TestStrategy` object as an argument, 
    invokes its `act()` method to perform the strategy's action, and then calls its `assert_()` 
    method to validate the expected behavior.

    Attributes:
    None

    Methods:
    execute(strategy: TestStrategy) -> None:
        Executes the action and validation steps of the provided strategy.
    """
    @classmethod
    def execute(cls, strategy: TestStrategy):
        """
        Executes the action and assertion of a given test strategy.

        This method performs the following steps:
        1. Calls the `act()` method of the provided strategy to perform its action.
        2. Calls the `assert_()` method of the provided strategy to validate the result.

        Args:
        strategy (TestStrategy): A strategy object that implements the `act()` and `assert_()` methods.

        Returns:
        None
        """
        # act
        strategy.act()

        # assert
        strategy.assert_()
