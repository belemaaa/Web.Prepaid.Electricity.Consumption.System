from rest_framework import permissions

class IsAdminUserOrReadOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True  # Allow read-only access to everyone
        return super().has_permission(request, view)
