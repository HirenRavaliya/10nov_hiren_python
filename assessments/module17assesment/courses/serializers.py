from rest_framework import serializers
from .models import Course


class CourseSerializer(serializers.ModelSerializer):
    """Full serializer for a Course object."""

    class Meta:
        model = Course
        fields = ['id', 'name', 'code', 'description', 'credits', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class CourseMinimalSerializer(serializers.ModelSerializer):
    """Lightweight serializer used inside the Student detail view."""

    class Meta:
        model = Course
        fields = ['id', 'name', 'code']
