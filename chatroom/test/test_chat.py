from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from chatroom.models import User, Messages
from django.contrib.auth.models import Group
from datetime import datetime
from freezegun import freeze_time


# @freeze_time("2022-06-12")
class ChatTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.group1 = Group.objects.create(name='first_test_group')
        cls.group2 = Group.objects.create(name='second_test_group')

        cls.user1 = User.objects.create_user(
            username='ali', email='a@a', password='1234')
        cls.user1.groups.set([cls.group1.id])

        cls.user2 = User.objects.create_user(
            username='sara', email='s@s', password='1234')
        cls.user2.groups.set([cls.group1.id, cls.group2.id])

        cls.user1.blockeduser.set([cls.user2.id])

        cls.user3 = User.objects.create_user(
            username='shima', email='sh@sh', password='1234')
        cls.user3.groups.set([cls.group1.id])

        """login
        cls.client = APIClient()
        cls.client.force_login(cls.user1)"""

        cls.message1 = Messages.objects.create(
            text='hi', group_message_id=str(cls.group1.id),
            user_message_id=str(cls.user1.id),
            date="2022-06-12T00:00:00Z"
        )
        cls.message2 = Messages.objects.create(
            text='hello', group_message_id=str(cls.group1.id),
            user_message_id=str(cls.user2.id),
            date="2022-06-13T00:00:00Z"
        )
        cls.message3 = Messages.objects.create(
            text='me', group_message_id=str(cls.group2.id),
            user_message_id=str(cls.user2.id),
            date="2022-06-12T00:00:00Z"
        )
        cls.message4 = Messages.objects.create(
            text='hey', group_message_id=str(cls.group1.id),
            user_message_id=str(cls.user3.id),
            date="2022-06-12T01:00:00Z"
        )

    def setUp(self):
        self.client.force_login(self.user1)

    # @freeze_time("2022-06-12")
    def test_create_message_successfully(self):
        # self.client.login(username='ali', password='1234')

        url = reverse('chat', kwargs={'pk': 1})
        data = {'text': 'bye', 'date': datetime.now()}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        current_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        message_date = response.data['date'].split('.')
        self.assertEqual(message_date[0], current_date)
        self.assertEqual(response.data['text'], 'bye')
        self.assertEqual(response.data['user_message'], self.user1.id)
        # how check group_message_id with response.data ?
        self.assertEqual(
            Messages.objects.get(text='bye').group_message_id, self.group1.id)
        # how check creation of a single obj ?
        self.assertEqual(Messages.objects.count(), 5)

    # @freeze_time("2022-06-12")
    def test_list_unread_unblocked_message_successfully(self):
        # self.assertEqual(datetime.now(), datetime(2022, 6, 12))

        url = reverse('chat', kwargs={'pk': 1})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        self.assertEqual(response.data[0]['text'], self.message1.text)
        self.assertEqual(response.data[0]['user_message'],
                         int(self.message1.user_message_id))
        self.assertEqual(response.data[0]['date'], self.message1.date)

        self.assertEqual(response.data[1]['text'], self.message4.text)
        self.assertEqual(response.data[1]['user_message'],
                         int(self.message4.user_message_id))
        self.assertEqual(response.data[1]['date'], self.message4.date)
        # check  messages order
        self.assertLessEqual(response.data[0]['date'], response.data[1]['date'])

    @freeze_time("2022-06-12")
    def test_list_read_unblocked_message_successfully(self):
        self.assertEqual(datetime.now(), datetime(2022, 6, 12))

        self.message1.status.set([self.user1.id])

        url = reverse('chat', kwargs={'pk': 1})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['text'], self.message4.text)

        message1_read_user = self.message1.status.all().values_list('id', flat=True)
        self.assertEqual(list(message1_read_user), [self.user1.id])

    def test_list_filter_message_text_right_value(self):
        url = reverse('chat', kwargs={'pk': 1}) + '?text=hello'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['text'], 'hello')

    def test_list_filter_message_text_wrong_value(self):
        url = reverse('chat', kwargs={'pk': 1}) + '?text=ss'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_list_filter_message_date_exact_available_value(self):
        # b'[{"text":"hi","date":"2022-06-12T00:00:00Z","user_message":1}]'
        url = reverse('chat', kwargs={'pk': 1}) + '?date=2022-06-12 00:00:00'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['text'], 'hi')

    def test_list_filter_message_date_exact_unavailable_value(self):
        url = reverse('chat', kwargs={'pk': 1}) + '?date=2022-06-18 00:00:00'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_list_filter_message_date_gte_available_value(self):
        url = reverse('chat', kwargs={'pk': 1}) + '?dategte=2022-06-13 00:00:00'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['text'], 'hello')

    def test_list_filter_message_date_gte_unavailable_value(self):
        url = reverse('chat', kwargs={'pk': 1}) + '?dategte=2022-06-18 00:00:00'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_list_filter_message_date_lte_available_value(self):
        url = reverse('chat', kwargs={'pk': 1}) + '?date__lte=2022-06-13 00:00:00'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['text'], 'hi')
        self.assertEqual(response.data[1]['text'], 'hey')
        self.assertEqual(response.data[2]['text'], 'hello')

    def test_list_filter_message_date_lte_unavailable_value(self):
        url = reverse('chat', kwargs={'pk': 1}) + '?date__lte=2022-06-10 00:00:00'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_list_filter_message_unavailable_query_param(self):
        url = reverse('chat', kwargs={'pk': 1}) + '?sth=2022-06-10 00:00:00'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['text'], 'hi')
        self.assertEqual(response.data[1]['text'], 'hey')
        self.assertEqual(response.data[2]['text'], 'hello')
