from factory import Faker, django
from authentication.models import User


class UserFactory(django.DjangoModelFactory):
    class Meta:
        model = User

    email = Faker("email")
    password = Faker('password')
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    home_address = Faker('address')
    
    # Adding next of kin fields
    next_of_kin_name = Faker('name')
    next_of_kin_contact = Faker('phone_number')
    next_of_kin_email = Faker('email')
    next_of_kin_relationship = Faker('random_element', elements=[relationship[0] for relationship in User.RELATIONSHIPS])
