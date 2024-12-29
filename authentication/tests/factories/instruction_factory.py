import factory
import random
from authentication.models import Instructor

from .user_factory import UserFactory
from .program_factory import ProgramFactory


class InstructorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Instructor

    user = factory.SubFactory(UserFactory, is_instructor=True)
    account_number = factory.Faker('numerify', text='##########')
    account_name = factory.Faker('name')
    bank_name = factory.Faker('company')