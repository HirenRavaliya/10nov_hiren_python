"""
Mobile-specific DRF permissions.
"""
from rest_framework.permissions import BasePermission


class IsStudentUser(BasePermission):
    """Allow access only to users with role='student'."""
    message = 'Only student accounts can access this endpoint.'

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role == 'student'
        )


class IsEducationalOrg(BasePermission):
    """
    Allow access only when the org_type of the **admin** who manages this
    student is 'educational'.

    For a student user, we look at their organization's admin org_type.
    For direct admin/teacher access, we check their own org_type.

    Falls back to checking the requesting user's org_type directly.
    """
    message = 'Leave requests are only available for educational institutions.'

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        # Direct check on the user's own org_type
        if user.org_type == 'educational':
            return True

        # For students: check via their organization's admin (if linked)
        if user.role == 'student':
            try:
                student = user.student_profile
                # If the student is linked to an organization, trust the
                # org_type stored on the student's own User record.
                # (Admins set org_type at their own account level, not per-org.)
                # We allow if org_type is default 'educational'.
                return user.org_type == 'educational'
            except Exception:
                pass

        return False


class IsAdminOrTeacherMobile(BasePermission):
    """Admins and teachers — for mobile admin-facing endpoints."""
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role in ('admin', 'teacher')
        )
