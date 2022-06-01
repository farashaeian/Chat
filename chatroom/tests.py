from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User


# example:
class UserTests(APITestCase):
    def test_create_user(self):
        """
        Ensure we can create a new user object.
        """
        url = reverse('user_register')
        data = {'name': 'sina', 'password': '1234'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().name, 'sina')

    def test_update_user(self):
        """
        Ensure we can update an exist user object.
        """
        url = reverse('add_user', kwargs={'pk': 4})  #  , args=[2] instead of kwargs is ok.
        data = {'groups': [1]}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get().name, 'sina')
        self.assertEqual(User.objects.get().groups, '1')

    def test_list_usergroups(self):
        """
                Ensure we can list user's groups.
                """
        url = reverse('user_groups')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GroupTest(APITestCase):
    def setUp(self):
        self.client.login(username='ali', password='1234')

    def test_list_group(self):
        url = reverse('group_register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
