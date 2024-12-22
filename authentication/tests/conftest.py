import pytest

from authentication.tests.factories import user_factory, program_factory, student_factory, instruction_factory


@pytest.fixture
def user_factory_fixture() -> user_factory.UserFactory:
    return user_factory.UserFactory

@pytest.fixture
def program_factory_fixture() -> program_factory.ProgramFactory:
    return program_factory.ProgramFactory

@pytest.fixture
def student_factory_fixture() -> student_factory.StudentFactory:
    return student_factory.StudentFactory

@pytest.fixture
def instructor_fixture() -> instruction_factory.InstructorFactory:
    return instruction_factory.InstructorFactory