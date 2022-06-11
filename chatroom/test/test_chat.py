from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from chatroom.models import User, Messages
from django.contrib.auth.models import Group
from collections import OrderedDict
from datetime import datetime


class ChatTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.group1 = Group.objects.create(name='first_test_group')
        cls.group2 = Group.objects.create(name='second_test_group')

        cls.user1 = User.objects.create_user(
            username='ali', email='a@a', password='1234')
        # Unresolved attribute reference 'user1' for class 'UserTests'
        cls.user1.groups.set([1])
        cls.user1.blockeduser.set([2])
        cls.user2 = User.objects.create_user(
            username='sara', email='s@s', password='1234')
        cls.user2.groups.set([1, 2])

        cls.message1 = Messages.objects.create(text='hi', group_message_id='1', user_message_id='1')
        cls.message2 = Messages.objects.create(text='hello', group_message_id='1', user_message_id='2')
        cls.message3 = Messages.objects.create(text='me', group_message_id='2', user_message_id='2')

    def test_create_message(self):
        self.assertTrue(self.client.login(username='ali', password='1234'))
        url = reverse('chat', kwargs={'pk': 1})
        data = {'text': 'bye'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Messages.objects.get(id=4).text, 'bye')
        self.assertEqual(Messages.objects.get(id=4).group_message_id, 1)
        self.assertEqual(Messages.objects.get(id=4).user_message_id, 1)
        self.assertEqual(Messages.objects.count(), 4)

    def test_list_message(self):
        self.assertTrue(self.client.login(username='ali', password='1234'))

        url = reverse('chat', kwargs={'pk': 1})  # kwargs={'pk': 1}{'text': 'hi'}, for filter test
        response = self.client.get(url)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # message date is changed!!!
        # self.assertEqual(response.data, [OrderedDict([('text', 'hi'), ('date', '2022-06-08T14:47:27.242568Z'), ('user_message', 1)])])
        self.assertEqual(len(response.data), 1)
        # why does show read message???
        """
        self.message1.status.set([1])
        self.assertEqual(len(response.data), 0)
        """

    def test_list_filter_message(self):
        self.assertTrue(self.client.login(username='ali', password='1234'))

        """text: true value"""
        response1 = self.client.get('/chat/1/?text=hello')
        response1.render()

        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        # message date is changed!!!
        # self.assertEqual(response.data, [OrderedDict([('text', 'hello'), ('date', '2022-06-08T14:47:27.242568Z'), ('user_message', 2)])])
        self.assertEqual(len(response1.data), 1)

        """text: wrong value"""
        response1 = self.client.get('/chat/1/?text=dd')
        response1.render()

        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response1.data), 0)

        """date of messages are changed"""
        """
        date filter test
        """