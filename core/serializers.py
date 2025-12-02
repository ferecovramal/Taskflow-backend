from rest_framework import serializers
from .models import Organization, User, Task, TaskHistory


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source='organization.name',read_only=True)

    class Meta:
        model = User
        fields = ['id','username','email','is_admin','organization','organization_name']

class TaskSerializer(serializers.ModelSerializer):
    assigned_users = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    assigned_usernames = serializers.StringRelatedField(many=True, read_only=True)
    organization_name = serializers.CharField(source='organization.name',read_only=True)

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'assigned_users',
            'assigned_usernames',
            'organization_name',
            'status',
            'organization',
            'deadline',
        ]
        read_only_fields = ['organization',]

    def validate_assigned_users(self, users):
        request_user = self.context['request'].user
        user_org = request_user.organization

        for user in users:
            if user.organization != user_org:
                raise serializers.ValidationError(
                    f"User '{user.username}' is not in your organization!"
                )
        return users

    def validate_status(self,value):
        if self.instance is None:
            return value

        old_status = self.instance.status
        new_status = value

        allowed = {
            "Pending" : ["InProgress"],
            "InProgress" : ["Completed"],
            "Completed" : [],
        }

        if new_status not in allowed[old_status]:
            raise serializers.ValidationError(
                f"Status '{old_status}' -> '{new_status}' kecidi icazeli deyil."
            )
        return value

class TaskHistorySerializer(serializers.ModelSerializer):
    changed_by_username = serializers.CharField(source = "changed_by.username", read_only=True)

    class Meta:
        model = TaskHistory
        fields   = "__all__"