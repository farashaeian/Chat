from .models import Messages, User
from .serializers import UserRegisterModelSerializer, GroupRegisterModelSerializer,\
    AddUserModelSerializer, UserGroupsModelSerializer, ChatModelSerializer, \
    BlockUserModelSerializer
from django.contrib.auth.models import Group
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .permissions import MessagePermission, BlockPermission
from rest_framework.pagination import LimitOffsetPagination
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
# import rest_framework_filters as filters


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


class BlockUser(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = BlockUserModelSerializer
    permission_classes = [BlockPermission]

    def get_serializer_context(self):
        context = super(BlockUser, self).get_serializer_context()
        context.update({"pk": self.request.user.id})
        return context


class MessageFilter(filters.FilterSet):
    class Meta:
        model = Messages
        fields = {
            'date': ['lte', 'gte', 'exact'],
            'text': ['exact'],
        }


class Chat(generics.ListCreateAPIView):
    model = Messages
    serializer_class = ChatModelSerializer
    permission_classes = [MessagePermission]
    filterset_class = MessageFilter
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        q = self.request.user.blockeduser.all()
        qids = q.values_list('id', flat=True)
        queryset = Messages.objects.filter(group_message_id=self.kwargs['pk']).exclude(
            status=self.request.user.id).exclude(
            user_message_id__in=qids)

        if self.request.query_params:
            queryset = Messages.objects.filter(group_message_id=self.kwargs['pk'])

        return queryset

    def list(self, request, *args, **kwargs):
        # to apply filters on queryset,
        # have to use filter_queryset() in overridden list method
        queryset = self.filter_queryset(self.get_queryset())
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


# def get_queryset() in chat view:
"""
if condition for filterclass queryset:
        query_txt = self.request.query_params.get('text')
        query_date = self.request.query_params.get('date')
        query_date_gte = self.request.query_params.get('date__gte')
        query_date_lte = self.request.query_params.get('date__lte')

        if query_txt or query_date or query_date_gte or query_date_lte:
            return ...proper queryset...
"""
"""
current group messages:

Messages.objects.filter(group_message_id=self.kwargs['pk'])
"""
"""
current group messages.unread messages for current user:

Messages.objects.filter(group_message_id=self.kwargs['pk']).exclude(
status=self.request.user.id)
"""
"""
current group messages.unread messages for current user.excepted
 the current user's blocked users messages:
 
 q = self.request.user.blockeduser.all()
 qids = q.values_list('id', flat=True)
            
Messages.objects.filter(group_message_id=self.kwargs['pk']).exclude(
                status=self.request.user.id).exclude(
                user_message_id__in=qids)
"""