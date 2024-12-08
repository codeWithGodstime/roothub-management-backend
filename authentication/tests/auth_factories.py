import factory
import random
from datetime import date

# , Student, Instructor, StudentPresentation
from authentication.models import User, Program
# from course.tests.course_factories import CourseFactory

from faker import Faker as FakerFactory

faker = FakerFactory()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.LazyAttribute(
        lambda o: f"user{random.randint(1, 10000)}@example.com")
    password = faker.password()


class ProgramFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Program
    duration = faker.random_int(1, 4)
    total_amount = faker.pydecimal(left_digits=7, min_value=50000, right_digits=2)

# class StudentFactory(factory.django.DjangoModelFactory):
#     """ students without sessions """
#     class Meta:
#         model = Student

#     user = factory.SubFactory(UserFactory)
#     course = factory.SubFactory(CourseFactory)
#     commencement_date = date.today() #
#     amount_paid = faker.pydecimal(left_digits=5, right_digits=2)


# class InstructorFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Instructor

#     user = factory.SubFactory(UserFactory)


# class StudentPresentationFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = StudentPresentation

#     student = factory.SubFactory(StudentFactory)
