from rest_framework.permissions import BasePermission

from courses.models import Course


class IsEnrolled(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.students.filter(pk=request.user.pk).exists()
