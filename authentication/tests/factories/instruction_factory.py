import factory
import random
from authentication.models import Instructor

from .user_factory import UserFactory
from .program_factory import ProgramFactory


class InstructorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Instructor

    user = factory.SubFactory(UserFactory)
    skills = factory.LazyFunction(
        lambda: random.sample(
            ["Python", "JavaScript", "UI/UX", "HTML", "CSS", "React"], 
            k=random.randint(1, 6)
        )
    )
    account_number = factory.Faker('numerify', text='##########')
    account_name = factory.Faker('name')
    bank_name = factory.Faker('company')