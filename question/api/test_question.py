from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from question.models import Question
from rest_framework import status
from rest_framework.authtoken.models import Token

from django.contrib.auth import get_user_model

User = get_user_model()

class QuestionAPITestCase(APITestCase):

	def staff_user(self):
		staff_user = User.objects.create(
			username='StaffUser',
			email='StaffUser@gmail.com',
			is_staff=True,
		)
		staff_user.set_password('Admin1')
		staff_user.save()

		url_login = reverse('account:login')
		data_login = {
			'username': 'StaffUser',
			'password': 'Admin1',
		}
		response = self.client.post(url_login, data_login, format='json')
		token = response.data.get('token')
		self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

	def no_staff_user(self):
		no_staff_user = User.objects.create(
			username='NoStaffUser',
			email='NoStaffUser@gmail.com',
			is_staff=False,
		)
		no_staff_user.set_password('OtherPassword1')
		no_staff_user.save()

		url_login = reverse('account:login')
		data_login = {
			'username': 'NoStaffUser',
			'password': 'OtherPassword1',
		}
		response = self.client.post(url_login, data_login, format='json')
		token = response.data.get('token')
		self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

	def test_check_create_user(self):
		self.staff_user()
		self.no_staff_user()
		staff_check = User.objects.get(username='StaffUser')
		no_staff_check = User.objects.get(username='NoStaffUser')
		self.assertEqual(staff_check.is_staff, True)
		self.assertEqual(no_staff_check.is_staff, False)




	" 						TESTS IN 			.../api/question/ 					"



	def test_staff_create_question_success(self):
		self.staff_user()
		url_question = reverse('question:list')
		data_question = {
			"question": "How are you?",
			"rank": 3
		}
		response_question = self.client.post(url_question, data_question, format='json')
		self.assertEqual(response_question.status_code, status.HTTP_201_CREATED)
		self.assertEqual(Question.objects.all().count(), 1)
		self.assertEqual(response_question.data.get('uri'), 'http://testserver/api/question/1/')
		url_detail = 'http://testserver' + reverse(
			'question:detail',
			kwargs={'id': Question.objects.get(question="How are you?").id}
		)
		self.assertEqual(response_question.data.get('uri'), url_detail)


	def test_no_staff_create_question_failed(self):
		self.no_staff_user()
		url_question = reverse('question:list')
		data_question = {
			"question": "How are you?",
			"rank": 3
		}
		response_question = self.client.post(url_question, data_question, format='json')
		self.assertEqual(response_question.status_code, status.HTTP_403_FORBIDDEN)
		self.assertEqual(response_question.data.get('detail'), 'You do not have permission to perform this action.')

	def test_staff_create_question_field_question_failed(self):
		self.staff_user()
		url_question = reverse('question:list')
		data_question = {
			"question": "Question without QUESTION MARK",
			"rank": 1
		}
		response_question = self.client.post(url_question, data_question, format='json')
		# print (response_question.data['question'][0])
		self.assertEqual(response_question.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(response_question.data.get('question')[0], "Please add '?' to your question.")

	def test_staff_create_question_field_rank_failed(self):
		self.staff_user()
		url_question = reverse('question:list')
		data_question = {
			"question": "How are you?",
			"rank": 10000
		}
		response_question = self.client.post(url_question, data_question, format='json')
		# print (response_question.data)
		self.assertEqual(response_question.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(response_question.data.get('rank')[0], '"10000" is not a valid choice.')

	def test_staff_create_question_field_failed(self):
		self.staff_user()
		url_question = reverse('question:list')
		data_question = {
			"rank": 10000
		}
		response_question = self.client.post(url_question, data_question, format='json')
		# print (response_question.data)
		self.assertEqual(response_question.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(response_question.data.get('question')[0], 'This field is required.')




	" 						TESTS IN 			.../api/question/<id>/ 					"

	def create_correct_question(self):
		url_question = reverse('question:list')
		data_question = {
			"question": "How are you?",
			"rank": 3
		}
		self.client.post(url_question, data_question, format='json')
		return Question.objects.get(question="How are you?").id

	def test_update_correct_question_success(self):
		self.staff_user()
		question_id = self.create_correct_question()
		url_question = reverse('question:detail', kwargs={'id':question_id})
		data_question_updated = {
			"question": "How are you UPDATED?",
			"rank": 3
		}
		response_update = self.client.put(url_question, data_question_updated, format='json')
		self.assertEqual(response_update.status_code, status.HTTP_200_OK)
		self.assertEqual(response_update.data.get('question'), "How are you UPDATED?")
		self.assertEqual(response_update.data.get('rank'), 3)
		self.assertEqual(Question.objects.get(id=question_id).question, "How are you UPDATED?")

	def test_update_correct_rank_success(self):
		self.staff_user()
		question_id = self.create_correct_question()
		url_question = reverse('question:detail', kwargs={'id':question_id})
		data_question_updated = {
			"question": "How are you?",
			"rank": 1
		}
		response_update = self.client.put(url_question, data_question_updated, format='json')
		self.assertEqual(response_update.status_code, status.HTTP_200_OK)
		self.assertEqual(response_update.data.get('rank'), 1)
		self.assertEqual(Question.objects.get(id=question_id).rank, 1)

	def test_update_correct_rank_failed(self):
		self.staff_user()
		question_id = self.create_correct_question()
		url_question = reverse('question:detail', kwargs={'id':question_id})
		data_question_updated = {
			"rank": 1
		}
		response_update = self.client.put(url_question, data_question_updated, format='json')
		self.assertEqual(response_update.status_code, status.HTTP_400_BAD_REQUEST)
		# print (response_update.data['question'][0])
		self.assertEqual(response_update.data.get('question')[0], 'This field is required.')


	def test_delete_correct_question_success(self):
		self.staff_user()
		question_id = self.create_correct_question()
		url_question = reverse('question:detail', kwargs={'id': question_id})
		response_delete = self.client.delete(url_question, format='json')
		# print(response_delete.data)
		self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)
		self.assertEqual(Question.objects.filter(id=question_id).exists(), False)