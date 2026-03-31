from django.contrib import admin
from .models import Doctor

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialty', 'hospital', 'city', 'experience_years', 'fee', 'is_available')
    list_filter = ('specialty', 'city', 'is_available')
    search_fields = ('name', 'hospital', 'city', 'email')
    list_editable = ('is_available', 'fee')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Personal Info', {'fields': ('name', 'email', 'phone')}),
        ('Professional Info', {'fields': ('specialty', 'hospital', 'city', 'experience_years', 'fee')}),
        ('Location', {'fields': ('latitude', 'longitude')}),
        ('Status', {'fields': ('is_available',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
    list_per_page = 20