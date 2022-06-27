from django.db import models
from datetime import datetime
from django.contrib.auth.models import Group, AbstractUser


class User(AbstractUser):
    blockeduser = models.ManyToManyField('self', symmetrical=False)  # related_name='blockedmember',

    class Meta:
        ordering = ['id']


class Messages(models.Model):
    text = models.TextField()
    date = models.DateTimeField(default=datetime.now, blank=False, null=False)
    group_message = models.ForeignKey(Group, on_delete=models.CASCADE)
    user_message = models.ForeignKey(User, related_name='username_message', on_delete=models.CASCADE)
    status = models.ManyToManyField(User)

    class Meta:
        ordering = ['date']
