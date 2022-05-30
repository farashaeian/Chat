from rest_framework import permissions
from .models import Messages
from django.contrib.auth.models import User, Group


class MessagePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(id=request.parser_context['kwargs']['pk']).exists():
            return True


class BlockPermission(permissions.BasePermission):
    message = 'pk!=request.user'

    def has_permission(self, request, view):
        # request.user.id is int
        # request.parser_context['kwargs']['pk'] is str
        if request.user.id == int(request.parser_context['kwargs']['pk']):
            return True
