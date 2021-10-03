from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class ViewsTests(APITestCase):

    def setUp(self):
        self.username = 'usuario'
        self.password = 'contrasegna'
        self.data = {
            'username': self.username,
            'password': self.password
        }

    def test_access_token(self):

        # URL using path name
        url = reverse('token_obtain_pair')

        # Create a user is a workaround in order to authentication works
        user = User.objects.create_user(username='usuario', email='usuario@mail.com', password='contrasegna')
        self.assertEqual(user.is_active, 1, 'Active User')

        # First post to get token
        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        token = response.data['access']
