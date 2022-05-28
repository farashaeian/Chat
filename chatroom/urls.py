from . import views
from django.urls import path

urlpatterns = [
        path('user_register/', views.UserRegister.as_view(), name='user_register'),
        path('group_register/', views.GroupRegister.as_view(), name='group_register'),
        path('add_user/<pk>/', views.AddUser.as_view(), name='add_user'),
        path('user_groups/', views.UserGroups.as_view(), name='user_groups'),
        path('chat/<pk>/', views.Chat.as_view(), name='chat'),
        path('block_user/<pk>/', views.BlockUser.as_view(), name='block_user'),
]

