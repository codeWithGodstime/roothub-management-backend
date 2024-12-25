import factory
import random

from faker import Faker

from authentication.tests.factories import instruction_factory, program_factory
from course.models import Course


faker = Faker()
_level= faker.random_element(elements=["Beginner", "Basic", "Intermediate", "Advanced"])

class CourseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Course

    instructor = factory.SubFactory(instruction_factory.InstructorFactory)
    program = factory.SubFactory(program_factory.ProgramFactory)

    @factory.lazy_attribute
    def name(self):
        program_name = self.program.name
        return f"{program_name}-{_level.lower()}"

    @factory.lazy_attribute
    def level(self):
        level_mapping = {
            "Beginner": 1,
            "Basic": 2,
            "Intermediate": 3,
            "Advanced": 4
        }
        return level_mapping[_level]
