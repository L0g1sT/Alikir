from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from datetime import timedelta
from http import HTTPStatus

from users.models import EmailVerification, User


class UserRegistrationViewTestCase(TestCase):
    def setUp(self):
        self.registration_data = {
                'first_name': 'susan',
                'last_name': 'coffey',
                'username': 'susan',
                'email': 'susan@yandex.ru',
                'password1': 'Ek5lmdup',
                'password2': 'Ek5lmdup'
                }
        self.path = reverse('users:registration')

    def test_user_registration_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Алькир - Регистрация')
        self.assertTemplateUsed(response, 'users/registration.html')

    def test_user_registration_post_success(self):
        username = self.registration_data['username']

        self.assertFalse(User.objects.filter(username=username).exists())
        
        response = self.client.post(self.path, self.registration_data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(User.objects.filter(username=username).exists())

        email_verification = EmailVerification.objects.filter(user__username=username)

        self.assertTrue(email_verification.exists())
        self.assertEqual(
                email_verification.first().expiration.date(),
                (now() + timedelta(hours=48)).date()
                )

    def test_user_registration_post_error(self):
        User.objects.create(username=self.registration_data['username'])
        response = self.client.post(self.path, self.registration_data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким именем существует.', html=True)
