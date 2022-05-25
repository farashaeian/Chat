import django_filters
from .models import Messages #, CustomUser
from .serializers import UserRegisterModelSerializer, GroupRegisterModelSerializer,\
    AddUserModelSerializer, UserGroupsModelSerializer, ChatModelSerializer, \
    SearchMessageModelSerializer
from django.contrib.auth.models import User, Group
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .permissions import MessagePermission
from rest_framework.response import Response
# from rest_framework.filters import SearchFilter
# from django_filters import FilterSet
from django_filters import rest_framework as filters
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend


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


class ChatPagination(LimitOffsetPagination):
    max_limit = 5


class FilterMessage(filters.FilterSet):
    date = django_filters.DateFilter(method=None)
    before_date = django_filters.DateFilter(field_name='date', lookup_expr='lte')
    after_date = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    text = filters.CharFilter(field_name='text', lookup_expr='exact')
    # method='text_queryset'

    class Meta:
        model = Messages
        fields = ['before_date', 'after_date', 'text', 'date']


class MessageFilter(filters.FilterSet):
    class Meta:
        model = Messages
        fields = {
            'date': ['lte', 'gte'],
            'text': ['exact'],
        }


class SearchMessage(generics.ListAPIView):
    serializer_class = SearchMessageModelSerializer
    permission_classes = [MessagePermission]
    # filter_backends = [SearchFilter]
    # search_fields = ['text']
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['text', 'date']
    filterset_class = MessageFilter
    # pagination_class = [LimitOffsetPagination]

    def get_queryset(self):
        return Messages.objects.filter(group_message_id=self.kwargs['pk'])


class Chat(generics.ListCreateAPIView):
    serializer_class = ChatModelSerializer
    permission_classes = [MessagePermission]
    filterset_class = MessageFilter
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Messages.objects.filter(group_message_id=self.kwargs['pk'])\
            #.exclude(            status=self.request.user.id)
    """ 
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ChatModelSerializer(queryset, many=True)
        # associate retrieved messages to the current user
        current_user = self.request.user
        current_user.messages_set.add(*queryset)
        current_user.save()
        return Response(serializer.data)
    """
    def get_serializer_context(self):
        context = super(Chat, self).get_serializer_context()
        context.update({"pk": self.kwargs['pk']})
        return context

