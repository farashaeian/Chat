from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from chatroom.models import User
from django.contrib.auth.models import Group


class UserTests(APITestCase):

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

    def test_create_user_successfully(self):
        """
        Ensure we can create a new user object.
        """
        url = reverse('user_register')
        data = {'username': 'sina', 'password': '1234'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)
        user = User.objects.get(username='sina')
        self.assertEqual(response.data['username'], user.username)
        self.assertEqual(response.data['password'], user.password)
        self.assertEqual(response.data['groups'], list(user.groups.all()))

    def test_update_add_user_successfully(self):
        """
        Ensure we can add a user to the groups.
        """
        # self.assertTrue(self.client.login(username='ali', password='1234'))
        # self.client.force_authenticate(user)

        url = reverse('add_user', kwargs={'pk': 1})  # args=[2] instead of kwargs is ok.
        data = {'groups': [1, 2]}
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['groups'],
                         list(self.user1.groups.all().values_list('id', flat=True)))

    def test_list_usergroups_successfully(self):
        """
        Ensure we can list users groups.
        """
        url = reverse('user_groups')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['username'], self.user1.username)
        self.assertEqual(response.data[0]['groups'],
                         list(self.user1.groups.all().values_list('id', flat=True)))
        self.assertEqual(response.data[1]['username'], self.user2.username)
        self.assertEqual(response.data[1]['groups'],
                         list(self.user2.groups.all().values_list('id', flat=True)))

    def test_update_block_user_successfully(self):
        """
        Ensure we can update blocked users for the current user object.
        """

        url = reverse('block_user', kwargs={'pk': 1})
        data = {'blockeduser': [2]}
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # check blockeduser.id (which one?)
        # 1
        q = self.user1.blockeduser.all()
        qid = q.values_list('id', flat=True)
        self.assertEqual(list(qid), [2])
        # 2
        self.assertEqual(response.data["blockeduser"], [2])
