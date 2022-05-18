# Generated by Django 4.0.4 on 2022-05-18 04:12

import datetime
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chatroom', '0002_alter_messages_date_alter_messages_user_message_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='messages',
            name='status',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='messages',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 18, 8, 42, 4, 817112)),
        ),
        migrations.DeleteModel(
            name='Status',
        ),
    ]