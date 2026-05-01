from rest_framework import serializers
from .models import DoctorLocation

class DoctorLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorLocation
        fields = '__all__'
