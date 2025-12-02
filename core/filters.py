from django_filters import rest_framework as filters
from.models import Task


class TaskFilter(filters.FilterSet):
    deadline_after = filters.DateTimeFilter(field_name='deadline', lookup_expr='gte')
    deadline_before = filters.DateTimeFilter(field_name='deadline', lookup_expr='lte')

    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    assigned_users = filters.NumberFilter(field_name = 'assigned_users__id')

    class Meta:
        model = Task
        fields = ['status','organization']