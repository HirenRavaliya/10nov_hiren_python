from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone', 'enrollment_date']
    search_fields = ['first_name', 'last_name', 'email']
    filter_horizontal = ['courses']
    list_filter = ['gender', 'enrollment_date']
    ordering = ['last_name', 'first_name']
