# Generated by Django 3.1.14 on 2022-05-28 09:52

import datetime
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatroom', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messages',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 28, 14, 22, 27, 131370)),
        ),
        migrations.AlterField(
            model_name='user',
            name='blockeduser',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
