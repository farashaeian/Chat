from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from django.http import request



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
    class Meta:
        model = User
        fields = ['groups']


class UserGroupsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'groups']


class ChatModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(ChatModelSerializer, self).__init__( *args, **kwargs)
        self.current_group_id = kwargs['context']['view'].kwargs['pk']

    user_message = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Messages
        fields = ['text', 'date', 'user_message']
        extra_kwargs = {
           'date': {'read_only': True},
        }

    def validate(self, attrs):
        group= Group.objects.get(id=self.current_group_id)
        attrs['group_message'] = group
        return attrs


