from django_filters import rest_framework as filters
from .models import Student


class StudentFilter(filters.FilterSet):
    program = filters.CharFilter(field_name='program__name', lookup_expr='icontains')

    class Meta:
        model = Student
        fields = ['type', 'program']