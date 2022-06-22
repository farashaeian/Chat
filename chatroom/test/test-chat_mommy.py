from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from chatroom.models import User, Messages
from django.contrib.auth.models import Group
from datetime import datetime
from freezegun import freeze_time
from model_mommy import mommy


class ChatCreateTests(APITestCase):
    def setUp(self):
        self.user = mommy.make(User)
        self.client.force_login(self.user)

        self.group = mommy.make(Group, 2)
        self.user.groups.set([self.group[0].id])

    def test_create_message_unsuccessfully(self):
        url = reverse('chat', kwargs={'pk': self.group[1].id})
        data = {'text': 'test_msg'}
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_message_successfully(self):
        url = reverse('chat', kwargs={'pk': self.group[0].id})
        data = {'text': 'test_msg'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        msg = Messages.objects.all()
        self.assertEqual(msg.count(), 1)
        self.assertEqual(msg[0].group_message_id, self.group[0].id)

        self.assertEqual(response.data['text'], data['text'])
        self.assertEqual(response.data['user_message'], self.user.id)

        current_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        message_date = response.data['date'].split('.')
        self.assertEqual(message_date[0], current_date)


class ChatOtherTests(APITestCase):
    def setUp(self):
        self.group = mommy.make(Group, 2)
        self.user = mommy.make(User, 3)
        self.message = mommy.make(Messages, 4)

        self.client.force_login(self.user[0])

        self.user[0].groups.set([self.group[0].id])
        self.user[0].blockeduser.set([self.user[1].id])
        self.user[1].groups.set([self.group[0].id, self.group[1].id])
        self.user[2].groups.set([self.group[0].id])






