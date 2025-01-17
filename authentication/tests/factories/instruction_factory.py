import factory
import random
from authentication.models import Instructor, Skill, InstructorSkill

from .user_factory import UserFactory
from .program_factory import ProgramFactory


class SkillFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Skill
    name = factory.Sequence(lambda n: f"{['Python', 'JavaScript', 'Java', 'C++', 'Ruby'][n % 5]}-{n}")


class InstructorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Instructor

    user = factory.SubFactory(UserFactory, is_instructor=True)
    account_number = factory.Faker("numerify", text="##########")
    account_name = factory.Faker("name")
    bank_name = factory.Faker("company")


class InstructorSkillFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = InstructorSkill
    
    instructor_id = factory.SubFactory(InstructorFactory)
    skill_id = factory.SubFactory(SkillFactory)
    is_primary = False