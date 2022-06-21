from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from chatroom.models import User
from django.contrib.auth.models import Group
from model_mommy import mommy


class GroupTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = mommy.make(User)

    def setUp(self):
        self.client.force_login(self.user)

    def test_create_group_successfully(self):
        url = reverse('group_register')
        data = {'name': 'test_group'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data['name'], 'test_group')

    def test_list_group_successfully(self):
        group = mommy.make(Group, 3)
        url = reverse('group_register')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['name'], group[0].name)
        self.assertEqual(response.data[1]['name'], group[1].name)
        self.assertEqual(response.data[2]['name'], group[2].name)

