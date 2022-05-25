from django.db import models
from datetime import datetime
from django.contrib.auth.models import User, Group, AbstractUser
from django.contrib.auth.base_user import BaseUserManager

"""
class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, **kwargs):
        user = self.model(username=username, is_active=True, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **kwargs):
        user = self.model(username=username, is_staff=True, is_superuser=True, is_active=True, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUser(User):
    block = models.ManyToManyField('self')
    objects = CustomUserManager
"""


class Messages(models.Model):
    text = models.TextField()
    date = models.DateTimeField(default=datetime.now(), blank=False, null=False)
    group_message = models.ForeignKey(Group, on_delete=models.CASCADE)
    user_message = models.ForeignKey(User, related_name='username_message', on_delete=models.CASCADE)
    status = models.ManyToManyField(User)

    class Meta:
        ordering = ['date']



