from rest_framework.decorators import action
from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Organization, User, Task, TaskHistory
from .serializers import OrganizationSerializer, UserSerializer, TaskSerializer, TaskHistorySerializer
from .permissions import IsSameOrganization, ReadOnlyPermission, IsOrganizationAdmin, IsOwnerOrReadOnly, \
    IsOwnerOrAdminOrSuperAdmin, CanChangeTaskStatus
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import TaskFilter


# Create your views here.

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsOwnerOrReadOnly |  ReadOnlyPermission]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Organization.objects.all()

        return Organization.objects.filter(id = user.organization_id)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [ IsOrganizationAdmin | IsSameOrganization]

    @action(detail = False, methods=["GET"], url_path= "me")
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return User.objects.all()

        if user.is_admin:
            return User.objects.filter(organization=user.organization)

        return User.objects.filter(id = user.id)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdminOrSuperAdmin()]
        return[IsAuthenticated()]


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsOwnerOrReadOnly | CanChangeTaskStatus]

    filter_backends = (DjangoFilterBackend,SearchFilter,OrderingFilter)
    filter_class = TaskFilter
    filterset_fields = ["status", "organization","assigned_users"]
    search_fields = ["title", "description"]
    ordering_fields = ["deadline", "created_at"]


    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Task.objects.all()

        return Task.objects.filter(organization=user.organization)

    def perform_create(self, serializer):
        serializer.save(organization=self.request.user.organization)


    def perform_update(self, serializer):
        old_task = Task.objects.get(pk=self.get_object().pk)
        new_task = serializer.save()

        user = self.request.user

        #Status deyisende tarixceye yaz
        if old_task.status != new_task.status:
            TaskHistory.objects.create(
                task = new_task,
                changed_by = user,
                field_name = "status",
                old_value = old_task.status,
                new_value = new_task.status
            )

           #Description deyisende
        if old_task.description != new_task.description:
            TaskHistory.objects.create(
                task = new_task,
                changed_by = user,
                field_name = "description",
                old_value = old_task.description,
                new_value = new_task.description
            )


        if old_task.deadline != new_task.deadline:
            TaskHistory.objects.create(
                task = new_task,
                changed_by = user,
                field_name = "deadline",
                old_value = old_task.deadline,
                new_value = new_task.deadline
            )

class TaskHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TaskHistory.objects.all()
    serializer_class = TaskHistorySerializer
    permission_classes = [IsAuthenticated]


