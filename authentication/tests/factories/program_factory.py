import factory
import faker

from authentication.models import Program


class ProgramFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Program

    name = factory.Iterator(["web development", 'python', 'data analysis', 'graphics design'])
    duration = factory.Faker(
        "random_element",
        elements=("1", "2", "3", "4")
    )
    total_amount = factory.Faker(
        "pydecimal",
        left_digits=6, 
        min_value=50000, 
        right_digits=2
    )