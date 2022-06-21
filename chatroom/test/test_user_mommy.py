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

    def setUp(self):
        self.client.force_login(self.user[0])

    def test_update_add_user_successfully(self):
        url = reverse('add_user', kwargs={'pk': self.group[0].id})

