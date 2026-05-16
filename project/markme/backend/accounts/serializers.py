from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from .models import Student, Teacher, Organization

User = get_user_model()


# ── JWT customization: add role + name to token payload ──────────────────────
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['full_name'] = user.full_name
        token['role'] = user.role
        token['email'] = user.email
        token['org_type'] = user.org_type  # 'educational' | 'company'
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['role'] = self.user.role
        data['full_name'] = self.user.full_name
        data['user_id'] = str(self.user.id)
        data['org_type'] = self.user.org_type  # 'educational' | 'company'
        return data


# ── User ─────────────────────────────────────────────────────────────────────
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'role', 'org_type', 'phone', 'profile_pic', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['email', 'full_name', 'role', 'org_type', 'phone', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)


# ── Organization ──────────────────────────────────────────────────────────────
class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'


# ── Teacher ───────────────────────────────────────────────────────────────────
class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role=User.TEACHER),
        source='user',
        write_only=True
    )
    student_count = serializers.SerializerMethodField()

    class Meta:
        model = Teacher
        fields = ['id', 'user', 'user_id', 'subject', 'organization', 'student_count', 'created_at']

    def get_student_count(self, obj):
        return obj.students.count()


class TeacherCreateSerializer(serializers.Serializer):
    """Create teacher user + profile in one call."""
    email = serializers.EmailField()
    full_name = serializers.CharField(max_length=150)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    password = serializers.CharField(write_only=True, min_length=8)
    subject = serializers.CharField(max_length=100, required=False, allow_blank=True)
    organization = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all(), required=False, allow_null=True)

    def create(self, validated_data):
        subject = validated_data.pop('subject', '')
        organization = validated_data.pop('organization', None)
        password = validated_data.pop('password')
        user = User.objects.create_user(
            email=validated_data['email'],
            full_name=validated_data['full_name'],
            phone=validated_data.get('phone', ''),
            role=User.TEACHER,
            password=password,
        )
        teacher = Teacher.objects.create(user=user, subject=subject, organization=organization)
        return teacher


# ── Student ───────────────────────────────────────────────────────────────────
class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    assigned_teacher_name = serializers.CharField(source='assigned_teacher.user.full_name', read_only=True, default=None)
    attendance_percentage = serializers.SerializerMethodField()
    total_present = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = [
            'id', 'user', 'roll_number', 'guardian_name', 'guardian_phone',
            'guardian_email', 'assigned_teacher', 'assigned_teacher_name',
            'organization', 'face_registered', 'profile_photo',
            'attendance_percentage', 'total_present', 'created_at'
        ]
        read_only_fields = ['id', 'face_registered', 'created_at']

    def get_attendance_percentage(self, obj):
        logs = obj.attendance_logs.all()
        if not logs.exists():
            return 0.0
        present = logs.filter(status='PRESENT').count()
        return round((present / logs.count()) * 100, 1)

    def get_total_present(self, obj):
        return obj.attendance_logs.filter(status='PRESENT').count()


class StudentCreateSerializer(serializers.Serializer):
    """Create student user + profile in one call."""
    email = serializers.EmailField()
    full_name = serializers.CharField(max_length=150)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    password = serializers.CharField(write_only=True, min_length=6)
    roll_number = serializers.CharField(max_length=50, required=False, allow_blank=True)
    guardian_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    guardian_phone = serializers.CharField(max_length=20)
    guardian_email = serializers.EmailField(required=False, allow_blank=True)
    assigned_teacher = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all(), required=False, allow_null=True)
    organization = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all(), required=False, allow_null=True)

    def create(self, validated_data):
        guardian_phone = validated_data.pop('guardian_phone')
        guardian_name = validated_data.pop('guardian_name', '')
        guardian_email = validated_data.pop('guardian_email', '')
        roll_number = validated_data.pop('roll_number', '')
        assigned_teacher = validated_data.pop('assigned_teacher', None)
        organization = validated_data.pop('organization', None)
        password = validated_data.pop('password')

        user = User.objects.create_user(
            email=validated_data['email'],
            full_name=validated_data['full_name'],
            phone=validated_data.get('phone', ''),
            role=User.STUDENT,
            password=password,
        )
        student = Student.objects.create(
            user=user,
            guardian_phone=guardian_phone,
            guardian_name=guardian_name,
            guardian_email=guardian_email,
            roll_number=roll_number,
            assigned_teacher=assigned_teacher,
            organization=organization,
        )
        return student


# ── FCM token update ──────────────────────────────────────────────────────────
class FCMTokenSerializer(serializers.Serializer):
    fcm_token = serializers.CharField()
