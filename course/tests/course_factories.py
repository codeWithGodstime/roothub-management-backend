import factory
import random
from factory import Faker
import factory.fuzzy
from course.models import Course, CourseSession, CourseSessionPayment, CourseTutor

from faker import Factory as FakerFactory

faker = FakerFactory.create()

    # Define the allowed course names
COURSE_CHOICES = [
    'Web Development',
    'Python Programming',
    'Visual Communication',
    'Data Analysis'
]

class CourseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Course

    name = factory.fuzzy.FuzzyChoice(choices=COURSE_CHOICES)
    total_amount = factory.Faker('pydecimal', left_digits=5, right_digits=2, positive=True)
    duration = factory.Faker('random_element', elements=['1', '2', '3', '4'])


