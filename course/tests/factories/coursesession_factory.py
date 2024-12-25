import factory
import random

from datetime import datetime, timedelta
from faker import Faker

from course.tests.factories import course_factory
from course.models import CourseSession


faker = Faker()

class CourseSessionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CourseSession

    start_date = factory.LazyFunction(lambda: datetime.now())
    estimated_end_date = factory.LazyFunction(lambda: datetime.now() + timedelta(days=30))
    end_date = None 
    course = factory.SubFactory(course_factory.CourseFactory)
    is_active = True
