"""
Custom User model supporting Admin (org staff), Teacher, and Student roles.
Students have a linked StudentProfile with biometric face encoding data.

org_type field on admin accounts controls which system version is shown:
  'educational' → full feature set including Leave Requests (default)
  'company'     → general organisation version without Leave Requests
"""
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import uuid


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', User.ADMIN)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ADMIN = 'admin'
    TEACHER = 'teacher'
    STUDENT = 'student'
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (TEACHER, 'Teacher'),
        (STUDENT, 'Student'),
    ]

    # Organisation type — controls which system version the admin sees.
    # 'educational': full feature set with Leave Requests (schools/colleges).
    # 'company': general org version without Leave Requests.
    ORG_EDUCATIONAL = 'educational'
    ORG_COMPANY = 'company'
    ORG_TYPE_CHOICES = [
        (ORG_EDUCATIONAL, 'Educational Institution'),
        (ORG_COMPANY, 'Company / Organisation'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=STUDENT)
    org_type = models.CharField(
        max_length=20,
        choices=ORG_TYPE_CHOICES,
        default=ORG_EDUCATIONAL,
        help_text='Only relevant for admin accounts. Determines the system version shown in the dashboard.'
    )
    phone = models.CharField(max_length=20, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    fcm_token = models.TextField(blank=True, help_text='Firebase Cloud Messaging token for push notifications')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = UserManager()

    class Meta:
        db_table = 'users'
        ordering = ['full_name']

    def __str__(self):
        return f'{self.full_name} ({self.role})'

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_teacher(self):
        return self.role == self.TEACHER

    @property
    def is_student_user(self):
        return self.role == self.STUDENT


class Organization(models.Model):
    """Represents a school/institute that uses Hajri Hub."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    logo = models.ImageField(upload_to='org_logos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    """Extended profile for teachers."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    subject = models.CharField(max_length=100, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True, related_name='teachers')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Teacher: {self.user.full_name}'


class Student(models.Model):
    """Extended profile for students with guardian contact info."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    roll_number = models.CharField(max_length=50, blank=True)
    guardian_name = models.CharField(max_length=150, blank=True)
    guardian_phone = models.CharField(max_length=20)
    guardian_email = models.EmailField(blank=True)
    assigned_teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    # Biometric data
    face_encoding = models.BinaryField(null=True, blank=True, help_text='Pickled numpy face encoding from face_recognition')
    face_registered = models.BooleanField(default=False)
    profile_photo = models.ImageField(upload_to='student_photos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Student: {self.user.full_name}'

    @property
    def name(self):
        return self.user.full_name
