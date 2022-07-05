from rest_framework import permissions

class MentorPermission(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_mentor)
