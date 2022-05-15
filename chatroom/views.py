from . import models
from . import serializers

from django.contrib.auth.models import User, Group
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .permissions import MessagePermission


class UserRegister(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserRegisterModelSerializer


class GroupRegister(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.GroupRegisterModelSerializer
    queryset = Group.objects.all()


class AddUser(generics.UpdateAPIView):
    queryset = User
    serializer_class = serializers.AddUserModelSerializer


class User_Groups(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = serializers.UserGroupsModelSerializer


class Chat(generics.ListCreateAPIView):
    permission_classes = [MessagePermission]
    serializer_class = serializers.ChatModelSerializer
    queryset = models.Messages.objects.all()

    def get_queryset(self):
        return models.Messages.objects.filter(group_message_id=self.kwargs['pk'])
"""

    def perform_create(self, serializer):
        serializer.save(user_message=self.request.user)
queryset=User.objects.all()
"""
"""
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
"""
