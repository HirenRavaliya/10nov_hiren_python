from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import messages
from q3.models import Doctor
from .serializers import DoctorSerializer

class DoctorPublicList(generics.ListAPIView):
    """Public endpoint — anyone can view doctor list (read-only)."""
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [AllowAny]

class DoctorProtectedList(generics.ListCreateAPIView):
    """Protected endpoint — requires token auth to CREATE doctors."""
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

class DoctorProtectedDetail(generics.RetrieveUpdateDestroyAPIView):
    """Protected endpoint — requires token auth to UPDATE/DELETE."""
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]

class CustomAuthToken(ObtainAuthToken):
    """POST username + password to get auth token."""
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.id, 'username': user.username})

def auth_ui(request):
    token = None
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            t, _ = Token.objects.get_or_create(user=user)
            token = t.key
            messages.success(request, f'Token obtained for {username}')
        else:
            error = 'Invalid credentials. Use Django admin to create a superuser.'
    doctors = Doctor.objects.all()
    return render(request, 'q13/auth.html', {'token': token, 'error': error, 'doctors': doctors})
