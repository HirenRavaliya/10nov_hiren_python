from rest_framework import serializers
from .models import Doctor

class DoctorSerializer(serializers.ModelSerializer):
    """Serializer for the Doctor model in doctor_finder app."""
    class Meta:
        model = Doctor
        fields = ['id', 'name', 'specialty', 'contact_email', 'contact_phone',
                  'hospital', 'city', 'available', 'latitude', 'longitude', 'created_at']
        read_only_fields = ['id', 'created_at']
