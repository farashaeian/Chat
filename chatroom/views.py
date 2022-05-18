from . import models
from . import serializers
from django.contrib.auth.models import User, Group
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .permissions import MessagePermission
from rest_framework.response import Response

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


class UserGroups(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = serializers.UserGroupsModelSerializer


class Chat(generics.ListCreateAPIView):
    queryset = models.Messages.objects.all()
    serializer_class = serializers.ChatModelSerializer
    permission_classes = [MessagePermission]

    def get_queryset(self):
        return models.Messages.objects.filter(group_message_id=self.kwargs['pk']).exclude(
            status=self.request.user.id)

    def List(self, request):
        queryset = self.get_queryset()
        serializer = serializers.ChatModelSerializer(queryset, many=True)
        return Response(serializer.data)


class AddStatus(generics.UpdateAPIView):
    queryset = models.Messages
    serializer_class = serializers.AddStatusModelSerializer
