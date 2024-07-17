from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .forms import SignUpForm
from django.urls import reverse

class UserRegistrationTest(TestCase):
    def test_user_registration(self):
        response = self.client.post(reverse('user:signup'), {
            'username': 'testuser',
            'email': 'test@example',
            'password1': 'password123',
            'password2': 'password123',
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists())

class UserLoginTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_user_login(self):
        response = self.client.post(reverse('user:login'), {
            'username': 'testuser',
            'password': 'password123',
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

class UserLogoutTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword123')

    def test_user_logout(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('user:logout'))

        self.assertEqual(response.status_code, 302)
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class SignUpFormTests(TestCase):

    def setUp(self):
        self.existing_user = User.objects.create_user(username='existinguser', email='existing@example.com', password='password123')
        self.form_data = {'username': 'testuser'}
        self.form = SignUpForm(data=self.form_data)
    
    def test_clean_username_unique(self):
        try:
            self.form.is_valid()
        except ValidationError as e:
            self.fail(f'ValidationError raised: {e}')
    
    def test_clean_email_unique(self):
        try:
            self.form.is_valid()
        except ValidationError as e:
            self.fail(f'ValidationError raised: {e}')
    
    def test_clean_username_not_unique(self):
        self.form_data['username'] = self.existing_user.username
        self.form = SignUpForm(data=self.form_data)
        self.assertRaises(ValidationError, self.form.is_valid)
    
    def test_clean_email_not_unique(self):
        self.form_data['email'] = self.existing_user.email
        self.form = SignUpForm(data=self.form_data)
        self.assertRaises(ValidationError, self.form.is_valid)