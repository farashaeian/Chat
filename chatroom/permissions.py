from rest_framework import permissions


class MessagePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(id=request.parser_context['kwargs']['pk']).exists():
            return True
