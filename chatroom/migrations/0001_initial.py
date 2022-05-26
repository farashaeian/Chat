# Generated by Django 3.1.14 on 2022-05-26 09:05

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('date', models.DateTimeField(default=datetime.datetime(2022, 5, 26, 13, 35, 55, 942017))),
                ('group_message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
                ('status', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('user_message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='username_message', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='BlockedUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blocklist_is_activ', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
