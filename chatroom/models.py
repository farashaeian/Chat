from django.db import models
from datetime import datetime
from django.contrib.auth.models import User, Group


class Messages(models.Model):
    text = models.TextField()
    date = models.DateTimeField(default=datetime.now(), blank=False, null=False)
    group_message = models.ForeignKey(Group, on_delete=models.CASCADE)
    user_message = models.ForeignKey(User, related_name='username_message', on_delete=models.CASCADE)
    status = models.ManyToManyField(User)

    class Meta:
        ordering = ['date']



