from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from chatroom.models import User
from django.contrib.auth.models import Group
from collections import OrderedDict


class GroupTests(APITestCase):

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

    def setUp(self):
        self.client.force_login(self.user1)

    def test_create_group_successfully(self):
        """
        Ensure we can create a new group object.
        """

        url = reverse('group_register')
        data = {'name': 'test_group'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Group.objects.count(), 3)
        self.assertEqual(response.data['name'], 'test_group')

    def test_list_group_successfully(self):
        # self.client.force_authenticate(self.user1)
        url = reverse('group_register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], self.group1.name)
        self.assertEqual(response.data[1]['name'], self.group2.name)

