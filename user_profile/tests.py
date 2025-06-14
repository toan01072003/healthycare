from django.urls import reverse
from rest_framework.test import APITestCase
from auth_service.models import User

class UserProfileTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='patient2@example.com', password='pass1234', role='patient', status='approved')

    def test_create_and_update_profile(self):
        url = reverse('userprofile-list')
        data = {
            'user': str(self.user.id),
            'full_name': 'Test Patient',
            'date_of_birth': '1990-01-01',
            'gender': 'male',
            'phone_number': '123456789',
            'address': '123 Street',
            'profile_photo': ''
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        profile_id = response.data['id']
        update_data = data.copy()
        update_data['address'] = '456 Avenue'
        update_response = self.client.put(reverse('userprofile-detail', args=[profile_id]), update_data, format='json')
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.data['address'], '456 Avenue')

    def test_my_profile_create_and_update(self):
        self.client.force_login(self.user)
        url = reverse('my-profile')
        data = {
            'full_name': 'Test Patient',
            'date_of_birth': '1990-01-01',
            'gender': 'male',
            'phone_number': '123456789',
            'address': '123 Street',
            'profile_photo': ''
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)

        update_data = data.copy()
        update_data['address'] = '789 Road'
        update_response = self.client.put(url, update_data, format='json')
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.data['address'], '789 Road')

