from rest_framework import permissions
from .models import Messages
from django.contrib.auth.models import User, Group


class MessagePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(id=request.parser_context['kwargs']['pk']).exists():
            return True


class BlockPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
