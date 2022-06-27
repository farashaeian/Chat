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


class ChatOther1Tests(APITestCase):
    def setUp(self):
        self.group = mommy.make(Group, 2)
        self.user = mommy.make(User, 3)

        self.client.force_login(self.user[0])

        self.user[0].groups.set([self.group[0].id])
        self.user[0].blockeduser.set([self.user[1].id])
        self.user[1].groups.set([self.group[0].id, self.group[1].id])
        self.user[2].groups.set([self.group[0].id])

        self.message0 = Messages.objects.create(
            text='hi', group_message_id=str(self.group[0].id),
            user_message_id=str(self.user[0].id),
            date="2022-06-12T00:00:00Z"
        )
        self.message1 = Messages.objects.create(
            text='hello', group_message_id=str(self.group[0].id),
            user_message_id=str(self.user[1].id),
            date="2022-06-13T00:00:00Z"
        )
        self.message2 = Messages.objects.create(
            text='me', group_message_id=str(self.group[1].id),
            user_message_id=str(self.user[1].id),
            date="2022-06-12T00:00:00Z"
        )
        self.message3 = Messages.objects.create(
            text='hey', group_message_id=str(self.group[0].id),
            user_message_id=str(self.user[2].id),
            date="2022-06-12T01:00:00Z"
        )

    def test_list_unread_unblocked_message_successfully(self):
        url = reverse('chat', kwargs={'pk': self.group[0].id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        self.assertEqual(response.data[0]['text'], self.message0.text)
        self.assertEqual(response.data[0]['user_message'],
                         int(self.message0.user_message_id))
        self.assertEqual(response.data[0]['date'], self.message0.date)

        self.assertEqual(response.data[1]['text'], self.message3.text)
        self.assertEqual(response.data[1]['user_message'],
                         int(self.message3.user_message_id))
        self.assertEqual(response.data[1]['date'], self.message3.date)
        # check  messages order
        self.assertLessEqual(response.data[0]['date'], response.data[1]['date'])

    def test_list_read_unblocked_message_successfully(self):
        self.message0.status.set([self.user[0].id])

        url = reverse('chat', kwargs={'pk': self.group[0].id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['text'], self.message3.text)

        message1_read_user = self.message3.status.all().values_list('id', flat=True)
        self.assertEqual(list(message1_read_user), [self.user[0].id])


class ChatOther2Tests(APITestCase):
    def setUp(self):
        self.group = mommy.make(Group, 2)
        self.user = mommy.make(User, 3)

        self.client.force_login(self.user[0])

        self.user[0].groups.set([self.group[0].id])
        self.user[0].blockeduser.set([self.user[1].id])
        self.user[1].groups.set([self.group[0].id, self.group[1].id])
        self.user[2].groups.set([self.group[0].id])

        self.message = mommy.make(Messages, 4)
        # , group_message=self.group, user_message=self.user

        self.message[0].group_message_id = self.group[0].id
        self.message[0].user_message_id = self.user[0].id

        self.message[1].group_message_id = self.group[0].id
        self.message[1].user_message_id = self.user[1].id

        self.message[2].group_message_id = self.group[1].id
        self.message[2].user_message_id = self.user[1].id

        self.message[3].group_message_id = self.group[0].id
        self.message[3].user_message_id = self.user[2].id

    def test_list_unread_unblocked_message_successfully(self):
        url = reverse('chat', kwargs={'pk': self.group[0].id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        self.assertEqual(response.data[0]['text'], self.message[0].text)
        self.assertEqual(response.data[0]['user_message'],
                         int(self.message[0].user_message_id))
        self.assertEqual(response.data[0]['date'], self.message[0].date)

        self.assertEqual(response.data[1]['text'], self.message[3].text)
        self.assertEqual(response.data[1]['user_message'],
                         int(self.message[3].user_message_id))
        self.assertEqual(response.data[1]['date'], self.message[3].date)
        # check  messages order
        self.assertLessEqual(response.data[0]['date'], response.data[1]['date'])

    def test_list_read_unblocked_message_successfully(self):
        self.message[0].status.set([self.user[0].id])

        url = reverse('chat', kwargs={'pk': self.group[0].id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['text'], self.message[3].text)

        message1_read_user = self.message[3].status.all().values_list('id', flat=True)
        self.assertEqual(list(message1_read_user), [self.user[0].id])
