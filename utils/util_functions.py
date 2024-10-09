import uuid
from faker import Faker

def generate_uuid():
    return str(uuid.uuid4())


def generate_passwords():
    return Faker().password()