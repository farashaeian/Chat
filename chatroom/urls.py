from . import views
from . import serializers
from . import models
from django.urls import path

urlpatterns = [
        path('user_register/', views.UserRegister.as_view(), name='user_register'),
        path('group_register/', views.GroupRegister.as_view(), name='group_register'),
        path('add_user/<pk>/', views.AddUser.as_view(), name='add_user'),
        path('chat/<pk>/', views.Chat.as_view(), name='chat'),
]
