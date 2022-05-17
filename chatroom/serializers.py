from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from django.http import request


class StatusModelSerializer(serializers.ModelSerializer):
    # (how?) fill user_message field with current group in the ChatModelSerializer
    class Meta:
        model = Status
        fields = ['message', 'user_status', 'status']


class UserRegisterModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'groups']
        extra_kwargs = {
            'User.password': {'write_only': True,
                              'style': {'input_type': 'password',}
                              }
        }

    def validate(self, attrs):
        attrs['password'] = make_password(attrs['password'])
        return attrs


class GroupRegisterModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']
        extra_kwargs = {
            'Group.permissions': {'read_only': True}
        }


class AddUserModelSerializer(serializers.ModelSerializer):
    #message_status = StatusModelSerializer(many=True)
    class Meta:
        model = User
        fields = ['groups']
       # fields = ['groups', 'message_status']
#    def create(self, validated_data):
 #       pass


class UserGroupsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'groups']


class ChatModelSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super(ChatModelSerializer, self).__init__( *args, **kwargs)
        self.current_group_id = kwargs['context']['view'].kwargs['pk']

    user_message = serializers.PrimaryKeyRelatedField(default=serializers.CurrentUserDefault(),queryset=User.objects.all())
    message_status = StatusModelSerializer(many=True)

    class Meta:
        model = Messages
        fields = ['text', 'date', 'user_message', 'message_status']
        extra_kwargs = {
            'date': {'read_only': True},
        }

    def validate(self, attrs):
        group= Group.objects.get(id=self.current_group_id)
        attrs['group_message'] = group

        member = User.objects.filter(groups=self.current_group_id)
        attrs['user_status'] = member
        #member = Status.objects.filter(user_status_groups=self.current_group_id)
        #attrs['user_status'] = member
        
        return attrs

    # When a user creates a message, an unread status must be created
    # for all group users for that message:
    def create(self, validated_data):
        message_status_data = validated_data.pop('message_status')
        message = Messages.objects.create(**validated_data)
        for msd in message_status_data:
            Status.objects.create(message=message, **msd)
        return message
