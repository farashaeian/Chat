from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from chatroom.models import User
from django.contrib.auth.models import Group
from model_mommy import mommy


class UserCreateTest(APITestCase):
    def test_create_user_successfully(self):
        group = mommy.make(Group)
        url = reverse('user_register')
        data = {'username': 'ali', 'password': '1234', 'groups': [group.id]}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_user = User.objects.all()
        self.assertEqual(created_user.count(), 1)
        self.assertEqual(response.data['username'], created_user[0].username)
        self.assertEqual(response.data['password'], created_user[0].password)
        
        self.assertEqual(
            response.data['groups'],
            [created_user[0].groups.get().id]
        )


class UserOtherTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.group = mommy.make(Group, 2)
        cls.user = mommy.make(User, 3)
        # , make_m2m=True, _fill_optional=True
        # groups=cls.group
        # make_m2m=True
        cls.user[1].groups.set([cls.group[0]])
        cls.user[2].groups.set([cls.group[0].id, cls.group[1].id])

    def setUp(self):
        self.client.force_login(self.user[0])

    def test_list_usergroups_successfully(self):
        url = reverse('user_groups')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user0_groups = list(self.user[0].groups.all().values_list('id', flat=True))
        self.assertEqual(response.data[0]['groups'], user0_groups)
        # self.assertEqual(response.data[0]['username'], self.user[0].username)

        user1_groups = list(self.user[1].groups.all().values_list('id', flat=True))
        self.assertEqual(response.data[1]['groups'], user1_groups)
        # self.assertEqual(response.data[1]['username'], self.user[1].username)

        user2_groups = list(self.user[2].groups.all().values_list('id', flat=True))
        self.assertEqual(response.data[2]['groups'], user2_groups)
        # self.assertEqual(response.data[2]['username'], self.user[2].username)

    def test_update_add_user_successfully(self):
        url = reverse('add_user', kwargs={'pk': self.user[1].id})
        data = {'groups': [1]}
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user1_groups = list(self.user[1].groups.all().values_list('id', flat=True))
        self.assertEqual(response.data['groups'], user1_groups)

    def test_update_block_user_successfully(self):
        url = reverse('block_user', kwargs={'pk': self.user[0].id})
        data = {'blockeduser': [2]}
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["blockeduser"], [2])

    def test_update_block_user_unsuccessfully_forbidden_user(self):
        url = reverse('block_user', kwargs={'pk': self.user[1].id})
        data = {'blockeduser': [2]}
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)






