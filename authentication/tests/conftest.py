import pytest

from authentication.tests.factories import user_factory, program_factory


@pytest.fixture
def user_factory_fixture() -> user_factory.UserFactory:
    return user_factory.UserFactory

@pytest.fixture
def program_factory_fixture() -> program_factory.ProgramFactory:
    return program_factory.ProgramFactory
