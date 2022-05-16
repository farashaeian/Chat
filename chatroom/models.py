from django.db import models
from datetime import datetime
from django.contrib.auth.models import User, Group


class Messages(models.Model):
    text = models.TextField()
    date = models.DateTimeField(default=datetime.now(), blank=False, null=False)
    group_message = models.ForeignKey(Group, on_delete=models.CASCADE)
    user_message = models.ForeignKey(User, related_name='username_message', on_delete=models.CASCADE)

    class Meta:
        ordering = ['date']

class Status(models.Model):
    message = models.ForeignKey(Messages, on_delete=models.CASCADE)
    user_status = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    status = models.BooleanField(default=False, blank=False, null=False)

