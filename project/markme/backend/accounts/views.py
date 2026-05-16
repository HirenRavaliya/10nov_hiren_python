import pickle
import numpy as np
import face_recognition
from PIL import Image
import io

from django.contrib.auth import get_user_model
from rest_framework import viewsets, generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.decorators import action

from .models import Student, Teacher, Organization
from .serializers import (
    UserSerializer, UserCreateSerializer, ChangePasswordSerializer,
    StudentSerializer, StudentCreateSerializer,
    TeacherSerializer, TeacherCreateSerializer,
    OrganizationSerializer, FCMTokenSerializer,
)
from .permissions import IsAdminOrTeacher, IsAdminUser

User = get_user_model()


# ── Auth & Profile ─────────────────────────────────────────────────────────────

class RegisterView(generics.CreateAPIView):
    """
    Public endpoint to self-register a student account.
    Admins/teachers are created from the admin panel or by another admin.
    """
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        # Force role to student for self-registration
        data = request.data.copy()
        data['role'] = User.STUDENT
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class MeView(generics.RetrieveUpdateAPIView):
    """Return/update the authenticated user's profile."""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({'detail': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'detail': 'Password changed successfully.'})


class UpdateFCMTokenView(APIView):
    """Mobile app registers its FCM token here for push notifications."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = FCMTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.fcm_token = serializer.validated_data['fcm_token']
        request.user.save(update_fields=['fcm_token'])
        return Response({'detail': 'FCM token updated.'})


# ── Organization ──────────────────────────────────────────────────────────────

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]


# ── Teacher ───────────────────────────────────────────────────────────────────

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.select_related('user', 'organization').all()
    permission_classes = [IsAdminOrTeacher]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    search_fields = ['user__full_name', 'subject']
    filterset_fields = ['organization']

    def get_serializer_class(self):
        if self.action == 'create':
            return TeacherCreateSerializer
        return TeacherSerializer

    def create(self, request, *args, **kwargs):
        serializer = TeacherCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        teacher = serializer.save()
        return Response(TeacherSerializer(teacher).data, status=status.HTTP_201_CREATED)


# ── Student ───────────────────────────────────────────────────────────────────

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.select_related('user', 'assigned_teacher__user', 'organization').all()
    permission_classes = [IsAdminOrTeacher]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    search_fields = ['user__full_name', 'roll_number', 'guardian_phone']
    filterset_fields = ['assigned_teacher', 'organization', 'face_registered']

    def get_serializer_class(self):
        if self.action == 'create':
            return StudentCreateSerializer
        return StudentSerializer

    def create(self, request, *args, **kwargs):
        serializer = StudentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        student = serializer.save()
        return Response(StudentSerializer(student).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def attendance_history(self, request, pk=None):
        """Attendance history for a single student (used by mobile app too)."""
        student = self.get_object()
        from attendance.models import AttendanceLog
        from attendance.serializers import AttendanceLogSerializer
        logs = AttendanceLog.objects.filter(student=student).order_by('-timestamp')
        serializer = AttendanceLogSerializer(logs, many=True)
        return Response(serializer.data)


# ── Face Enrollment ───────────────────────────────────────────────────────────

class EnrollFaceView(APIView):
    """
    POST /api/accounts/students/<uuid>/enroll-face/
    Accepts a photo (multipart), computes the 128-D face encoding via
    face_recognition, and stores it as binary in the Student record.
    """
    permission_classes = [IsAdminOrTeacher]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, pk):
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response({'detail': 'Student not found.'}, status=status.HTTP_404_NOT_FOUND)

        photo = request.FILES.get('photo')
        if not photo:
            return Response({'detail': 'No photo file provided.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            img = Image.open(photo).convert('RGB')
            img_array = np.array(img)

            encodings = face_recognition.face_encodings(img_array)
            if len(encodings) == 0:
                return Response(
                    {'detail': 'No face detected in the image. Please use a clear, well-lit frontal photo.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if len(encodings) > 1:
                return Response(
                    {'detail': 'Multiple faces detected. Please use a photo with only one person.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            encoding = encodings[0]
            # Serialize encoding as bytes using pickle
            student.face_encoding = pickle.dumps(encoding)
            student.face_registered = True

            # Also save the photo
            if request.FILES.get('photo'):
                student.profile_photo.save(
                    f'student_{student.id}.jpg',
                    photo,
                    save=False
                )

            student.save()
            return Response({
                'detail': 'Face enrolled successfully.',
                'face_registered': True,
                'student_id': str(student.id),
            })

        except Exception as e:
            return Response({'detail': f'Error processing image: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
