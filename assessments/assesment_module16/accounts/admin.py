from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Follow


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'get_role_display', 'is_staff', 'date_joined']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'groups']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    fieldsets = UserAdmin.fieldsets + (
        ('WriteSphere Profile', {
            'fields': ('bio', 'avatar', 'website')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Profile', {
            'fields': ('email', 'first_name', 'last_name', 'bio', 'avatar', 'website')
        }),
    )

    @admin.display(description='Role')
    def get_role_display(self, obj):
        return obj.get_role()



@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['follower', 'following', 'created_at']
    list_filter = ['created_at']
    search_fields = ['follower__username', 'following__username']
