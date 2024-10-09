import factory
import random
from factory import Faker
from authentication.models import User, Student, Instructor, StudentPresentation

from faker import Factory as FakerFactory

faker = FakerFactory.create()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.LazyAttribute(lambda o: f"user{random.randint(1, 10000)}@example.com") 
    password = faker.password()


class StudentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Student

    user = factory.SubFactory(UserFactory)


class InstructorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Instructor

    user = factory.SubFactory(UserFactory)


class StudentPresentationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = StudentPresentation
    
    student = factory.SubFactory(StudentFactory)