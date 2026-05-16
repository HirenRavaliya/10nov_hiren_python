from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    """Only admin-role users."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'admin')


class IsAdminOrTeacher(BasePermission):
    """Admins and teachers."""
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated
            and request.user.role in ('admin', 'teacher')
        )


class IsOwnerOrAdmin(BasePermission):
    """Object-level: owner of the resource, or admin."""
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        # Check if the object belongs to the requesting user
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return False
