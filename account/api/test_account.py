from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token

from django.contrib.auth import get_user_model

User = get_user_model()

class UserAPITestCase(APITestCase):
	def setUp(self):
		user = User.objects.create(
			username='55650',
			email='USOSuser1@gmail.com'
		)
		user.set_password('Lol123')
		user.save()

	def test_create_user(self):
		qs = User.objects.all().count()
		self.assertEqual(qs,1)

	def test_register_user_success_api(self):
		url = reverse('account:register')
		data = {
			'username'			: '55651',
			'email'				: 'USOSuser2@gmail.com',
			'password'			: 'Lol123',
			'confirm_password'	: 'Lol123',
		}
		response = self.client.post(url, data, format='json')
		# print(response.data['response']['token'])
		# print(response.data)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertGreater(len(response.data['response']['token']), 0)
		registered_user = User.objects.get(username=response.data['response']['user']['username'])
		self.assertEqual(registered_user.is_admin, False)
		self.assertEqual(registered_user.is_staff, False)

	def test_register_user_failed_email_api(self):
		url = reverse('account:register')
		data = {
			'username'			: '55651',
			'email'				: 'USOSuser1@gmail.com', #same email as in setUp
			'password'			: 'Lol123',
			'confirm_password'	: 'Lol123',
		}
		response = self.client.post(url, data, format='json')
		# print(response.data['email'], '\n\n')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(response.data['email'][0], 'my user with this email address already exists.')

	def test_register_user_failed_password_api(self):
		url = reverse('account:register')
		data = {
			'username'			: '55651',
			'email'				: 'USOSuser2@gmail.com',
			'password'			: 'Lol123',
			'confirm_password'	: 'Lol123123', #no matching passwords
		}
		response = self.client.post(url, data, format='json')
		# print(response.data['non_field_errors'][0])
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(response.data['non_field_errors'][0], 'Passwords must match.')

	def test_register_user_failed_password2_api(self):
		url = reverse('account:register')
		data = {
			'username'			: '55650',
			'email'				: 'USOSuser2@gmail.com',
			'password'			: 'Lol123', #without confirming password

		}
		response = self.client.post(url, data, format='json')
		# print(response.data)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(response.data['confirm_password'][0], "This field is required.")

	def test_register_user_failed_by_authenticated_user_api(self):
		url = reverse('account:register')
		data = {
			'username'			: '55650',
			'password'			: 'Lol123',
		}
		user = User.objects.get(username='55650')
		self.client.force_authenticate(user=user)
		response_for_authenticated_user = self.client.post(url, data, format='json')
		# print(response_for_authenticated_user.data)
		self.assertEqual(response_for_authenticated_user.status_code, status.HTTP_403_FORBIDDEN)
		self.assertEqual(response_for_authenticated_user.data['detail'], 'You are already logged')

	def test_login_user_by_username_success_api(self):
		url = reverse('account:login')
		data = {
			'username'			: '55650',
			'password'			: 'Lol123',
		}
		response = self.client.post(url, data, format='json')
		# print(response.data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['user']['username'], '55650')

	def test_login_user_by_email_success_api(self):
		url = reverse('account:login')
		data = {
			'username'			: 'USOSuser1@gmail.com',
			'password'			: 'Lol123',
		}
		response = self.client.post(url, data, format='json')
		# print(response.data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['user']['username'], '55650')

	def test_login_user_failed_api(self):
		url = reverse('account:login')
		data = {
			'username'			: 'NonExistingUser',
			'password'			: 'Lol123',
		}
		response = self.client.post(url, data, format='json')
		# print(response.data)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
		self.assertEqual(response.data['detail'], 'Invalid credential')


	def test_login_user_failed_by_same_credentials_api(self):
		url = reverse('account:login')
		data = {
			'username'			: '55650',
			'password'			: 'Lol123',
		}
		user = User.objects.get(username='55650')
		self.client.force_authenticate(user=user)
		response_for_authenticated_user = self.client.post(url, data, format='json')
		self.assertEqual(response_for_authenticated_user.status_code, status.HTTP_403_FORBIDDEN)
		self.assertEqual(response_for_authenticated_user.data['detail'], 'You are already logged')







