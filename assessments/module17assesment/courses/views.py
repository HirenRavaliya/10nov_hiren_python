from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Course
from .serializers import CourseSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Course CRUD.

    GET    /api/courses/          – list all courses
    POST   /api/courses/          – create a course
    GET    /api/courses/{id}/     – retrieve a course
    PUT    /api/courses/{id}/     – full update
    PATCH  /api/courses/{id}/     – partial update
    DELETE /api/courses/{id}/     – delete a course
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
