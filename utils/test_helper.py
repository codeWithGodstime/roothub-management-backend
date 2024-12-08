from typing import Literal
from faker import Faker
from datetime import date, timedelta

faker = Faker()


class TestHelper:

    def _student_data(self, program_id:str = None):

        return {
            "user": self._user_data(),        
            "type": faker.random_choices(elements=['INTERN', 'EXTERN', "TRIPTERN"])[0],
            "program": program_id,
            "payment_plan": faker.random_choices(elements=["FULL", "PART"])[0]
        }
    
    def _staff_data(self):
        user = self._user_data()
        user['is_staff'] = True   
        return user 
    
    def _instructor_data(self):
        return {
            "user": {
                "email": faker.email(),
                "first_name": faker.first_name(),
                "last_name": faker.last_name()
            }
        }

    def _course_data(self):
        return {
            "name": faker.random_choices(elements=["web development", 'python', 'data analysis', 'graphics design'])[0],
            "total_amount": faker.pydecimal(left_digits=7, min_value=50000, right_digits=2),
            "duration": faker.random_choices(elements=[x for x in range(1, 4)])[0]
        }
    
    def _user_data(self):
        return {
                "email": faker.email(),
                "first_name": faker.first_name(),
                "last_name": faker.last_name(),
                "next_of_kin_contact": faker.basic_phone_number()[:11],
                "home_address": faker.street_address(),
                "next_of_kin_name": faker.name(),
                "next_of_kin_email": faker.email(),
                "next_of_kin_relationship": "SISTER"
            }
    
    def _program_data(self):
        return {
            "name": faker.random_choices(elements=["web development", 'python', 'data analysis', 'graphics design'])[0],
            "duration": faker.random_choices(elements=[x for x in range(1, 4)])[0],
            "total_amount": float(faker.pydecimal(left_digits=7, min_value=30000, right_digits=2)),
        }

    def generate_test_data(self, type: Literal["user", "instructor", "student", 'program', "staff"], *args, **kwargs):
        program_id = None
        if args:
            program_id = args[0].id # this will get the id of the queryset
        # if type == 'student' and args:
        #     course_id = args[0].get("course_id")
        #     return self._student_data(course_id=course_id)

        
        if type == 'instructor':
            return self._instructor_data()
        elif type == 'staff':
            return self._staff_data()
        elif type == 'user':
            return self._user_data()
        elif type == 'program':
            return self._program_data()
        elif type == 'student':
            return self._student_data(program_id)
        
    @staticmethod
    def compare_dict_data(received:dict, expected:list):
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
