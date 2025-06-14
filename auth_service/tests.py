from django.urls import reverse
from rest_framework.test import APITestCase
from auth_service.models import User

class AuthServiceTests(APITestCase):
    def test_register_and_login_roles(self):
        register_url = reverse('register')
        login_url = reverse('login')

        for role in ['patient', 'doctor', 'nurse', 'lab_staff']:
            with self.subTest(role=role):
                email = f'{role}@example.com'
                data = {'email': email, 'password': 'pass1234', 'role': role}
                response = self.client.post(register_url, data, format='json')
                self.assertEqual(response.status_code, 200)
                self.assertTrue(User.objects.filter(email=email).exists())

                user = User.objects.get(email=email)
                user.status = 'approved'
                user.save()

                login_response = self.client.post(login_url, {'email': email, 'password': 'pass1234'}, format='json')
                self.assertEqual(login_response.status_code, 200)
                self.assertEqual(login_response.json().get('role'), role)

