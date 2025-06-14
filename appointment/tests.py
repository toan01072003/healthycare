from django.urls import reverse
from rest_framework.test import APITestCase
from auth_service.models import User
from user_profile.models import UserProfile


class AppointmentChatbotTests(APITestCase):
    def setUp(self):
        self.patient = User.objects.create_user(
            email='pat@example.com', password='pass1234', role='patient', status='approved'
        )
        self.doctor = User.objects.create_user(
            email='doc@example.com', password='pass1234', role='doctor', status='approved'
        )
        UserProfile.objects.create(
            user=self.doctor,
            full_name='Dr. Example',
            date_of_birth='1980-01-01',
            gender='male',
            phone_number='123',
            address='abc'
        )
        self.client.force_login(self.patient)

    def test_quick_select_booking_flow(self):
        url = reverse('chatbot-appointment')
        response = self.client.post(url, {
            'date_input': '2030-01-01T10:00',
            'doctor_input': 'Dr. Example'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Do you confirm', response.context['bot_message'])

        # confirm the appointment
        response = self.client.post(url, {
            'message': 'yes'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('has been confirmed', response.context['bot_message'])

        from appointment.models import Appointment
        self.assertEqual(Appointment.objects.count(), 1)
        appt = Appointment.objects.first()
        self.assertEqual(appt.doctor, self.doctor)

        # doctor should see the appointment in their schedule
        self.client.logout()
        self.client.force_login(self.doctor)
        schedule_url = reverse('doctor-schedule')
        response = self.client.get(schedule_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Confirmed via chatbot')

