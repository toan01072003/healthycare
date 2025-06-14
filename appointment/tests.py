from django.urls import reverse
from rest_framework.test import APITestCase
from auth_service.models import User
from user_profile.models import UserProfile
from appointment.models import Appointment
from django.utils import timezone


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

        # Confirm the appointment
        response = self.client.post(url, {'message': 'yes'})
        self.assertEqual(response.status_code, 200)

        appt = Appointment.objects.first()
        self.assertIsNotNone(appt)
        self.assertNotEqual(appt.patient_id, appt.doctor_id)
        self.assertEqual(appt.doctor_id, self.doctor.id)


class AppointmentActionTests(APITestCase):
    def setUp(self):
        self.patient = User.objects.create_user(
            email='testpat@example.com', password='pass1234', role='patient', status='approved'
        )
        self.doctor = User.objects.create_user(
            email='testdoc@example.com', password='pass1234', role='doctor', status='approved'
        )
        UserProfile.objects.create(
            user=self.doctor,
            full_name='Dr. Action',
            date_of_birth='1980-01-01',
            gender='male',
            phone_number='123',
            address='abc'
        )
        self.appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            date_time=timezone.now() + timezone.timedelta(days=1),
            reason='test',
            status='pending'
        )

    def test_patient_cancel(self):
        self.client.force_login(self.patient)
        url = reverse('cancel-appointment', args=[self.appointment.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.status, 'cancelled')

    def test_doctor_accept(self):
        self.client.force_login(self.doctor)
        url = reverse('respond-appointment', args=[self.appointment.id, 'accept'])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.status, 'confirmed')

    def test_doctor_reject(self):
        self.client.force_login(self.doctor)
        url = reverse('respond-appointment', args=[self.appointment.id, 'reject'])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.status, 'cancelled')



