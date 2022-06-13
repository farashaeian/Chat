from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from chatroom.models import User, Messages
from django.contrib.auth.models import Group
from collections import OrderedDict
from datetime import datetime
from freezegun import freeze_time


@freeze_time("2022-06-12")
class ChatTests(APITestCase):
    @classmethod
    @freeze_time("2022-06-12")
    def setUpTestData(cls):
        cls.group1 = Group.objects.create(name='first_test_group')
        cls.group2 = Group.objects.create(name='second_test_group')

        cls.user1 = User.objects.create_user(
            username='ali', email='a@a', password='1234')
        # Unresolved attribute reference 'user1' for class 'UserTests'
        cls.user1.groups.set([cls.group1.id])
        cls.user1.blockeduser.set([cls.group2.id])
        cls.user2 = User.objects.create_user(
            username='sara', email='s@s', password='1234')
        cls.user2.groups.set([cls.group1.id, cls.group2.id])

        cls.message1 = Messages.objects.create(
            text='hi', group_message_id=str(cls.group1.id), user_message_id=str(cls.user1.id))
        cls.message2 = Messages.objects.create(
            text='hello', group_message_id=str(cls.group1.id), user_message_id=str(cls.user2.id))
        cls.message3 = Messages.objects.create(
            text='me', group_message_id=str(cls.group2.id), user_message_id=str(cls.user2.id))

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

    @freeze_time("2022-06-12")
    def test_list_message(self):
        # datetime.now doesn't work in freezing
        a = datetime.now()
        b = datetime(2022, 6, 12)
        self.assertEqual(datetime.now(), datetime(2022, 6, 12))

        self.assertTrue(self.client.login(username='ali', password='1234'))

        url = reverse('chat', kwargs={'pk': 1})
        response = self.client.get(url)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        # message date is changed!!!
        self.assertEqual(
            response.data, [OrderedDict([('text', 'hi'), ('date', '2022-06-12'), ('user_message', 1)])])

        # show read message???
        self.message1.status.set([self.user1.id])
        self.assertEqual(len(response.data), 0)

        q = self.message1.status.all()
        qid = q.values_list('id', flat=True)
        self.assertEqual(list(qid), [self.message1.id])

    def test_list_filter_message(self):
        self.assertTrue(self.client.login(username='ali', password='1234'))

        # text: available value
        url = reverse('chat', kwargs={'pk': 1}) + '?text=hello'
        response = self.client.get(url)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        # text: non-available value
        url1 = reverse('chat', kwargs={'pk': 1}) + '?text=ss'
        response1 = self.client.get(url1)
        response1.render()

        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response1.data), 0)

        # date: exact:
        url2 = reverse('chat', kwargs={'pk': 1}) + '?date=2022-06-12 12:26:57.349857'
        response2 = self.client.get(url2)
        response2.render()

        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response2.data), 1)

        # date: gte:
        url3 = reverse('chat', kwargs={'pk': 1}) + '?date__gte=2022-06-12 12:26:57.349857'
        response3 = self.client.get(url3)
        response3.render()

        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response3.data), 12)

        # date: lte:
        url4 = reverse('chat', kwargs={'pk': 1}) + '?date__lte=2022-06-12 12:26:57.349857'
        response4 = self.client.get(url4)
        response4.render()

        self.assertEqual(response4.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response4.data), 1)
