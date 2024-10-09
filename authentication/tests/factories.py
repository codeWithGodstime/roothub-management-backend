import factory
from authentication.models import User, Student, Instructor, StudentPresentation

from faker import Factory as FakerFactory

faker = FakerFactory.create()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

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