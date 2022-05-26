from .models import Messages, BlockedUser
from .serializers import UserRegisterModelSerializer, GroupRegisterModelSerializer,\
    AddUserModelSerializer, UserGroupsModelSerializer, ChatModelSerializer, \
    BlockUserModelSerializer
from django.contrib.auth.models import User, Group
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .permissions import MessagePermission
from django_filters import rest_framework as filters
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response


class UserRegister(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterModelSerializer
    permission_classes = [IsAuthenticated]


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


class BlockUser(generics.ListCreateAPIView):
    queryset = BlockedUser.objects.all()
    serializer_class = BlockUserModelSerializer
    permission_classes = [IsAuthenticated]


class MessageFilter(filters.FilterSet):
    class Meta:
        model = Messages
        fields = {
            'date': ['exact', 'lte', 'gte'],
            'text': ['exact'],
        }


class Chat(generics.ListCreateAPIView):
    serializer_class = ChatModelSerializer
    permission_classes = [MessagePermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Messages.objects.filter(group_message_id=self.kwargs['pk'])
        # return Messages.objects.filter(group_message_id=self.kwargs['pk']).exclude(status=self.request.user.id)

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
