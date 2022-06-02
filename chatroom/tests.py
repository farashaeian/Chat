from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User
from rest_framework.test import APIClient


# example:
class UserTests(APITestCase):
    def setUp(self):
        # self.client.login(username='ali', password='1234')
        # user = User.objects.get(username='ali')
        user = None
        # client.login(username='ali', password='1234')
        self.client.force_login(user=user)

    def test_create_user(self):
        """
        Ensure we can create a new user object.
        """
        url = reverse('user_register')
        data = {'username': 'sina', 'password': '1234'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'sina')

    def test_update_add_user(self):
        """
        Ensure we can update groups field in an exist user object.
        """
        url = reverse('add_user', kwargs={'pk': 4})  #  , args=[2] instead of kwargs is ok.
        data = {'groups': [1]}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get().username, 'sina')
        self.assertEqual(User.objects.get().groups, '1')

    def test_update_block_user(self):
        """
        Ensure we can update groups field in an exist user object.
        """
        url = reverse('block_user', kwargs={'pk': 4})
        data = {'blockeduser': [1]}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # check permission
        self.assertEqual(User.objects.get().id, '4')
        # check blockeduser.id
        q = User.blockeduser.all()
        qid = q.values_list('id', flat=True)
        self.assertEqual(qid, '1')

    def test_list_usergroups(self):
        """
        Ensure we can list user's groups.
        """
        url = reverse('user_groups')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GroupTest(APITestCase):
    def setUp(self):
        # self.client.login(username='ali', password='1234')
        user = User.objects.get(username='ali', password='1234')
        # client.login(username='ali', password='1234')
        self.client.force_login(user=user)  # user=None

    def test_create_group(self):
        """
        Ensure we can create a new group object.
        """
        url = reverse('group_register')
        data = {'name': 'first_grou'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().name, 'first_group')

    def test_list_group(self):
        url = reverse('group_register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

