from rest_framework import serializers
from courses.serializers import CourseMinimalSerializer
from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    """
    Full Student serializer.

    - On READ  : `courses` returns nested course objects.
    - On WRITE : `course_ids` accepts a list of course primary keys.
    """

    courses = CourseMinimalSerializer(many=True, read_only=True)
    course_ids = serializers.PrimaryKeyRelatedField(
        source='courses',
        many=True,
        write_only=True,
        required=False,
        queryset=__import__('courses.models', fromlist=['Course']).Course.objects.all(),
    )
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Student
        fields = [
            'id',
            'first_name',
            'last_name',
            'full_name',
            'email',
            'phone',
            'gender',
            'date_of_birth',
            'enrollment_date',
            'courses',
            'course_ids',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'full_name', 'enrollment_date', 'created_at', 'updated_at']


class StudentListSerializer(serializers.ModelSerializer):
    """Compact serializer for list endpoints."""

    full_name = serializers.ReadOnlyField()
    course_count = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['id', 'full_name', 'email', 'enrollment_date', 'course_count']

    def get_course_count(self, obj):
        return obj.courses.count()
