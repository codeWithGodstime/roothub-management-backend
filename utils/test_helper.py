from typing import Literal
from faker import Faker
from datetime import date, timedelta

faker = Faker()


class TestHelper:

    def _student_data(self, course_id:str = None):

        return {
            "user": {
                "email": faker.email(),
                "first_name": faker.first_name(),
                "last_name": faker.last_name()
            },
            "address": faker.street_address(),
            "phone_number": faker.basic_phone_number()[:11], # enforce the generated phone number to be 11 digits
            "has_paid": True,
            "commencement_date": faker.date_between(start_date=date.today()),
            "course": course_id, #since we can create a student without a course id
            "type": faker.random_choices(elements=['INTERN', 'EXTERN'])[0],
            "amount_paid": faker.pydecimal(left_digits=7, min_value=30000, right_digits=2),
            "payment_status": faker.random_choices(elements=["FULL", "PART"])[0]
        }
    
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
                "last_name": faker.last_name()
            }

    def generate_test_data(self, type: Literal["user", "instructor", "student", 'course'], *args, **kwargs):

        if type == 'student' and args:
            course_id = args[0].get("course_id")
            return self._student_data(course_id=course_id)
        
        if type == 'instructor':
            return self._instructor_data()
        elif type == 'user':
            return self._user_data()
        elif type == 'course':
            return self._course_data()