from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Task

User = get_user_model()

class UserSummarySerializer(serializers.ModelSerializer):
    """
    Lightweight nested serializer for representing user in tasks
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class TaskSerializer(serializers.ModelSerializer):
    """
    Task serializer with nested user summary (Forward Relationship)
    """
    user = UserSummarySerializer(read_only=True)

    class Meta:
        model = Task
        fields = [
            'id', 
            'user', 
            'title', 
            'description', 
            'is_completed', 
            'created_at', 
            'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def validate_title(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters long.")
        return value


class UserSerializer(serializers.ModelSerializer):
    """
    User serializer with nested tasks (Reverse Relationship: One-to-Many)
    """
    full_name = serializers.SerializerMethodField()
    # 🚀 Nested Serializer: User has many Tasks
    tasks = TaskSerializer(many=True, read_only=True)
    task_count = serializers.IntegerField(source='tasks.count', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 
            'username', 
            'email', 
            'first_name', 
            'last_name', 
            'full_name', 
            'tasks', 
            'task_count', 
            'date_joined'
        ]
        read_only_fields = ['id', 'date_joined']

    def get_full_name(self, obj):
        name = f"{obj.first_name} {obj.last_name}".strip()
        return name if name else obj.username
