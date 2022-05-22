from .models import Messages
from .serializers import UserRegisterModelSerializer, GroupRegisterModelSerializer, AddUserModelSerializer, UserGroupsModelSerializer, ChatModelSerializer
from django.contrib.auth.models import User, Group
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .permissions import MessagePermission
from rest_framework.response import Response
from rest_framework.filters import SearchFilter


class UserRegister(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterModelSerializer


class GroupRegister(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupRegisterModelSerializer
    permission_classes = [IsAuthenticated]


class AddUser(generics.UpdateAPIView):
    queryset = User
    serializer_class = AddUserModelSerializer


class UserGroups(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserGroupsModelSerializer
    permission_classes = [IsAuthenticated]


class Chat(generics.ListCreateAPIView):
    queryset = Messages.objects.all()
    serializer_class = ChatModelSerializer
    permission_classes = [MessagePermission]
    filter_backends = [SearchFilter]
    search_fields = ['text']

    def get_queryset(self):
        return Messages.objects.filter(group_message_id=self.kwargs['pk']).exclude(
            status=self.request.user.id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ChatModelSerializer(queryset, many=True)
        # associate retrieved messages to the current user
        current_user = self.request.user
        current_user.messages_set.add(*queryset)
        current_user.save()
        return Response(serializer.data)

    def get_serializer_context(self):
        context = super(Chat, self).get_serializer_context()
        context.update({"pk": self.kwargs['pk']})
        return context


