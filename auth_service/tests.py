from django.urls import reverse
from rest_framework.test import APITestCase
from auth_service.models import User

class AuthServiceTests(APITestCase):
    def test_register_and_login_patient(self):
        register_url = reverse('register')
        data = {'email': 'patient@example.com', 'password': 'pass1234', 'role': 'patient'}
        response = self.client.post(register_url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(email='patient@example.com').exists())
        user = User.objects.get(email='patient@example.com')
        user.status = 'approved'
        user.save()
        login_url = reverse('login')
        login_response = self.client.post(login_url, {'email': 'patient@example.com', 'password': 'pass1234'}, format='json')
        self.assertEqual(login_response.status_code, 200)
        self.assertEqual(login_response.json().get('role'), 'patient')

