from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Student, Teacher, Organization


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'full_name', 'role', 'org_type', 'is_active', 'date_joined')
    list_filter = ('role', 'org_type', 'is_active', 'is_staff')
    search_fields = ('email', 'full_name')
    ordering = ('full_name',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('full_name', 'phone', 'role', 'org_type', 'profile_pic')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'role', 'org_type', 'password1', 'password2'),
        }),
    )


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'roll_number', 'guardian_phone', 'face_registered', 'assigned_teacher')
    list_filter = ('face_registered', 'organization')
    search_fields = ('user__full_name', 'roll_number', 'guardian_phone')


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'subject', 'organization')
    search_fields = ('user__full_name', 'subject')


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_email', 'contact_phone', 'created_at')
    search_fields = ('name',)
