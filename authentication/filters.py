from django_filters import rest_framework as filters
from .models import Student, Instructor


class StudentFilter(filters.FilterSet):
    program = filters.CharFilter(field_name='program__name', lookup_expr='icontains')

    class Meta:
        model = Student
        fields = ['type', 'program']


class InstructorFilter(filters.FilterSet):
    skill = filters.CharFilter(field_name="skills__name", lookup_expr="iexact")

    class Meta:
        model = Instructor
        fields = ["skill"]