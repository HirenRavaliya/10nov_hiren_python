from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Student
from .serializers import StudentSerializer, StudentListSerializer
from courses.models import Course
from courses.serializers import CourseSerializer


class StudentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Student CRUD + course-enrolment actions.

    Standard CRUD:
      GET    /api/students/          – list students (compact)
      POST   /api/students/          – create student
      GET    /api/students/{id}/     – retrieve student (full detail)
      PUT    /api/students/{id}/     – full update
      PATCH  /api/students/{id}/     – partial update
      DELETE /api/students/{id}/     – delete student

    Extra actions:
      GET    /api/students/{id}/courses/              – list enrolled courses
      POST   /api/students/{id}/enroll/               – enrol in a course
      DELETE /api/students/{id}/unenroll/{course_id}/ – remove from a course
    """

    queryset = Student.objects.prefetch_related('courses').all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return StudentListSerializer
        return StudentSerializer

    # ── Extra actions ──────────────────────────────────────────────────────

    @action(detail=True, methods=['get'], url_path='courses')
    def courses(self, request, pk=None):
        """List all courses a student is enrolled in."""
        student = self.get_object()
        serializer = CourseSerializer(student.courses.all(), many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='enroll')
    def enroll(self, request, pk=None):
        """
        Enrol a student in a course.
        Body: { "course_id": <int> }
        """
        student = self.get_object()
        course_id = request.data.get('course_id')

        if not course_id:
            return Response(
                {'error': 'course_id is required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            return Response(
                {'error': f'Course with id {course_id} not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        if student.courses.filter(pk=course_id).exists():
            return Response(
                {'message': f'Student is already enrolled in "{course.name}".'},
                status=status.HTTP_200_OK,
            )

        student.courses.add(course)
        return Response(
            {'message': f'Successfully enrolled in "{course.name}".'},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=['delete'], url_path=r'unenroll/(?P<course_id>\d+)')
    def unenroll(self, request, pk=None, course_id=None):
        """Remove a student from a course."""
        student = self.get_object()

        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            return Response(
                {'error': f'Course with id {course_id} not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        if not student.courses.filter(pk=course_id).exists():
            return Response(
                {'error': 'Student is not enrolled in this course.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        student.courses.remove(course)
        return Response(
            {'message': f'Removed from "{course.name}".'},
            status=status.HTTP_200_OK,
        )
