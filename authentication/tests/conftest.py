import pytest

from authentication.tests.factories import instruction_factory

pytestmark = pytest.mark.django_db


@pytest.fixture
def skill_fixture() -> instruction_factory.SkillFactory:
    return instruction_factory.SkillFactory

@pytest.fixture
def instructor_skills_fixture() -> instruction_factory.InstructorSkillFactory:
    return instruction_factory.InstructorSkillFactory