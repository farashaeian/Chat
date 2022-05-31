from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User
from .views import GroupRegister
from rest_framework.test import APIRequestFactory
from django.contrib.auth.hashers import make_password
from rest_framework.test import force_authenticate


# example:
class UserTests(APITestCase):
    def test_create_user(self):
        """
        Ensure we can create a new user object.
        """
        url = reverse('user_register')
        data = {'name': 'sina'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().name, 'sina')


class UserTestPost(APIRequestFactory):
    factory = APIRequestFactory()
    p = make_password(1234)
    request = factory.post('/user_register/', {'username': 'reza', 'password': p},
                           format='json')


class GroupTestPut(APIRequestFactory):
    factory = APIRequestFactory()
    request = factory.put('/add_user/4/', {'groups': [1,2]})


class GroupTestAuth(APIRequestFactory):
    factory = APIRequestFactory()
    user = User.objects.get(username='olivia')
    view = GroupRegister.as_view()

    # Make an authenticated request to the view...
    request = factory.get('/group_register/')
    force_authenticate(request, user=user)
    response = view(request)

