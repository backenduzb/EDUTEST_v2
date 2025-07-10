from rest_framework.permissions import IsAuthenticated

class IsTeacherUser(IsAuthenticated):
    def has_permission(self, request, view):
        if super().has_permission(request, view) and request.user and request.user.is_teacher:
            return True
        return False

class IsStudentUser(IsAuthenticated):
    def has_permission(self, request, view):
        if super().has_permission(request, view) and request.user and request.user.is_student:
            return True
        return False

class IsAdminUser(IsAuthenticated):
    def has_permission(self, request, view):
        if super().has_permission(request, view) and request.user and request.user.is_superuser:
            return True
        return False