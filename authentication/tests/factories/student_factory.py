import factory
from authentication.models import Student

from .user_factory import UserFactory
from .program_factory import ProgramFactory


class StudentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Student

    user = factory.SubFactory(UserFactory, is_student=True)
    type = factory.Iterator(['INTERN', 'EXTERN', 'TRIPTERN'])
    payment_plan = factory.Iterator(['FULL', 'PART', 'NOT PAID'])
    program = factory.SubFactory(ProgramFactory)