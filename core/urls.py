from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import OrganizationViewSet, UserViewSet, TaskViewSet, TaskHistoryViewSet

router = DefaultRouter()
router.register(r'organizations', OrganizationViewSet)
router.register(r'users', UserViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'task-history', TaskHistoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]