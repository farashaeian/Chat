from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User, Messages
from rest_framework.test import APIClient
from django.contrib.auth.models import Group


class UserTests(APITestCase):
    """
    def setUp(self):
        # creating user in setUp makes error for create_user test
        user = User.objects.create_user('ali', '1234')
        # self.assertTrue(self.client.login(username='ali', password='1234'))
        self.client.force_authenticate(user)"""

    def test_create_user(self):
        """
        Ensure we can create a new user object.
        """
        # creating user in setUp makes error for this test
        url = reverse('user_register')
        data = {'username': 'sina', 'password': '1234'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'sina')

    def test_update_add_user(self):
        """
        Ensure we can update groups field in an existing user object.
        """
        group = Group.objects.create(name='test_group')
        user = User.objects.create_user(username='ali', email='a@a', password='1234')
        self.assertTrue(self.client.login(username='ali', password='1234'))
        # self.client.force_authenticate(user)
        url = reverse('add_user', kwargs={'pk': 1})  # args=[2] instead of kwargs is ok.
        data = {'groups': [1]}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get().username, 'ali')
        # how to check user's groups?
        # self.assertEqual(User.objects.get().groups, '1')
        self.assertEqual(response.data, {'groups': [1]})

    def test_list_usergroups(self):
        """
        Ensure we can list user's groups.
        """
        url = reverse('user_groups')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_block_user(self):
        """
        Ensure we can update groups field in an existing user object.
        """
        b_user = User.objects.create_user(username='sara', email='s@s', password='1234')
        user = User.objects.create_user(username='ali', email='a@a', password='1234')
        self.assertTrue(self.client.login(username='ali', password='1234'))
        url = reverse('block_user', kwargs={'pk': 2})
        data = {'blockeduser': [1]}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # how check permission? (below line is wrong)
        """
        # self.assertEqual(User.objects.get().id, '2')"""
        # check blockeduser.id
        """
        q = User.blockeduser.all()
        qid = q.values_list('id', flat=True)
        self.assertEqual(qid, '1')"""
        self.assertEqual(response.data, {'blockeduser': [1]})
        self.assertEqual(User.objects.get().blockeduser_id, 1)


class GroupTests(APITestCase):
    """
    def setUp(self):
        # user = User.objects.get(username='ali', password='1234')
        # self.client.force_login(user=user)
        """

    def test_create_group(self):
        """
        Ensure we can create a new group object.
        """
        user = User.objects.create_user(username='ali', email='a@a', password='1234')
        self.assertTrue(self.client.login(username='ali', password='1234'))
        # self.client.force_authenticate(user)
        url = reverse('group_register')
        data = {'name': 'first_group'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Group.objects.count(), 1)
        self.assertEqual(Group.objects.get().name, 'first_group')

    def test_list_group(self):
        user = User.objects.create_user(username='ali', email='a@a', password='1234')
        # self.assertTrue(self.client.login(username='ali', password='1234'))
        self.client.force_authenticate(user)
        url = reverse('group_register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ChatTests(APITestCase):
    def test_create_message(self):
        group1 = Group.objects.create(name='first_test_group')
        group2 = Group.objects.create(name='second_test_group')
        user1 = User.objects.create_user(username='ali', email='a@a', password='1234')
        user1.groups.set([1, 2])
        user2 = User.objects.create_user(username='sara', email='s@s', password='1234')
        user2.groups.set([1])
        self.assertTrue(self.client.login(username='ali', password='1234'))
        url = reverse('chat', kwargs={'pk': 2})
        data = {'text': 'hi'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Messages.objects.get().text, 'hi')
        self.assertEqual(Messages.objects.get().group_message_id, 2)
        self.assertEqual(Messages.objects.get().user_message_id, 1)
        # what are these???
        # self.assertEqual(response.data, {'text': 'hi'})
        # self.assertEqual(json.loads(response.content), {'text': 'hi'})
        # {'text': 'hi', 'date': '2022-06-07T13:50:15.418753Z', 'user_message': 1}

    def test_list_message(self):
        messages = Messages.objects.filter(group_message=1)
        # why User.objects.get(id=4) can't work???
        user = User.objects.filter(id=4)
        self.assertTrue(self.client.login(username='ali', password='1234'))
