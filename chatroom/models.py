from django.db import models
from datetime import datetime
from django.contrib.auth.models import User, Group


class Messages(models.Model):
    text = models.TextField()
    date = models.DateTimeField(default=datetime.now(), blank=False, null=False)
    group_message = models.ForeignKey(Group, on_delete=models.CASCADE)
    user_message = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['date']
