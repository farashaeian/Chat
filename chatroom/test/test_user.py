from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from chatroom.models import User, Messages
from django.contrib.auth.models import Group
from collections import OrderedDict


class UserTests(APITestCase):

    @classmethod
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

    def test_create_user(self):
        """
        Ensure we can create a new user object.
        """
        # creating user in setUp affect this test
        url = reverse('user_register')
        data = {'username': 'sina', 'password': '1234'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)
        user = User.objects.get(username='sina')
        self.assertEqual(response.data, {'username': 'sina', 'password': user.password, 'groups': []})

    def test_update_add_user(self):
        """
        Ensure we can update groups field in an existing user object.
        """
        self.assertTrue(self.client.login(username='ali', password='1234'))
        # self.client.force_authenticate(user)
        url = reverse('add_user', kwargs={'pk': 1})  # args=[2] instead of kwargs is ok.
        data = {'groups': [1, 2]}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(User.objects.get().username, ['ali', 'sara', 'sina'])
        # how to check user's groups?
        # 1
        q = self.user1.groups.all()
        qid = q.values_list('id', flat=True)
        self.assertEqual(list(qid), [1, 2])
        # 2
        self.assertEqual(response.data, {'groups': [1, 2]})

    def test_list_usergroups(self):
        """
        Ensure we can list user's groups.
        """
        url = reverse('user_groups')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [OrderedDict([('username', 'ali'), ('groups', [1])]), OrderedDict([('username', 'sara'), ('groups', [1, 2])])])

    def test_update_block_user(self):
        """
        Ensure we can update groups field in an existing user object.
        """
        self.assertTrue(self.client.login(username='ali', password='1234'))
        url = reverse('block_user', kwargs={'pk': 1})
        data = {'blockeduser': [2]}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # how check permission? (below line is wrong)
        # check blockeduser.id (which one?)
        # 1
        q = self.user1.blockeduser.all()
        qid = q.values_list('id', flat=True)
        self.assertEqual(list(qid), [2])
        # 2
        self.assertEqual(response.data, {"blockeduser": [2]})
