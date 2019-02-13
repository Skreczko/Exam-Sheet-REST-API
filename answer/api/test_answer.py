from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from question.models import Question
from answer.models import Answer, UserAnswer
from rest_framework import status
from rest_framework.authtoken.models import Token

from django.contrib.auth import get_user_model

User = get_user_model()

class AnswerAPITestCase(APITestCase):

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

	def create_question(self):
		self.staff_user()
		url_question = reverse('question:list')
		data_question1 = {
			"question": "First question?",
			"rank": 1
		}
		self.client.post(url_question, data_question1, format='json')




	" 										STAFF 										"

	def create_staff_answer(self):
		self.create_question()
		url_answer = reverse('answer:admin-list')
		question = Question.objects.all().first().id
		data_answer_false = {
			"question"			: question,
			"answer_question"	: "Incorrect answer",
			"is_correct"		: False,
		}
		return self.client.post(url_answer, data_answer_false, format='json')

	def test_creating_answer_success(self):
		answer_false = self.create_staff_answer()
		question = Question.objects.all().first().id

		self.assertEqual(Answer.objects.all().count(), 1)
		self.assertEqual(answer_false.status_code, status.HTTP_201_CREATED)
		self.assertEqual(answer_false.data.get('is_correct'), False)
		self.assertEqual(answer_false.data.get('question'), question)

	def test_creating_answer_quesion_field_failed(self):
		self.create_question()
		url_answer = reverse('answer:admin-list')
		data_answer_false = {
			"answer_question"	: "Incorrect answer",
			"is_correct"		: False,
		}

		response_answer_false = self.client.post(url_answer, data_answer_false, format='json')
		# print (response_answer_false.data)
		self.assertEqual(response_answer_false.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(response_answer_false.data.get('question')[0], 'This field is required.')

	def test_creating_answer_field_failed(self):
		self.create_question()
		url_answer = reverse('answer:admin-list')
		question = Question.objects.all().first().id
		data_answer_false = {
			"question"			: question,
			"is_correct"		: False,
		}

		response_answer_false = self.client.post(url_answer, data_answer_false, format='json')
		# print (response_answer_false.data)
		self.assertEqual(response_answer_false.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(response_answer_false.data.get('answer_question')[0], 'This field is required.')

	def test_update_answer_success(self):
		answer_false = self.create_staff_answer()
		answer = Answer.objects.all().first()
		url_update = reverse('answer:admin-detail', kwargs={'id': answer.id})
		data_answer_false = {
			"answer_question"	: "Incorrect answer EDITED",
			"is_correct"		: True,
		}
		response_answer_update = self.client.put(url_update, data_answer_false, format='json')
		# print (response_answer_update.data)
		self.assertEqual(response_answer_update.status_code, status.HTTP_200_OK)
		self.assertEqual(response_answer_update.data.get('answer_question'), 'Incorrect answer EDITED')
		self.assertEqual(response_answer_update.data.get('is_correct'), True)

	def test_delete_answer_success(self):
		answer_false = self.create_staff_answer()
		answer = Answer.objects.all().first()
		url_delete = reverse('answer:admin-detail', kwargs={'id': answer.id})

		response_answer_delete = self.client.delete(url_delete, format='json')
		# print (response_answer_delete.data)
		self.assertEqual(response_answer_delete.status_code, status.HTTP_204_NO_CONTENT)
		self.assertEqual(Answer.objects.all().exists(), False)

	def test_getting_UserAnswer_list_as_no_staff(self):
		answer_false = self.create_staff_answer()

		answer = Answer.objects.all().first()
		url_update = reverse('answer:list')

		print(self.request.user)

		response_answer_get = self.client.get(url_update,  format='json')
		# print (response_answer_get.data)
		self.assertEqual(response_answer_get.status_code, status.HTTP_403_FORBIDDEN)
		self.assertEqual(response_answer_get.data.get('detail'), 'You do not have permission to perform this action.')

	# def test_getting_UserAnswer_detail_as_no_staff(self):
	# 	answer_false = self.create_staff_answer()
	# 	self.staff_user()
	# 	answer = Answer.objects.all().first()
	# 	url_update = reverse('answer:detail', kwargs={'id': answer.id})
	#
	# 	response_answer_get = self.client.get(url_update,  format='json')
	# 	# print (response_answer_get.data)
	# 	self.assertEqual(response_answer_get.status_code, status.HTTP_403_FORBIDDEN)
	# 	self.assertEqual(response_answer_get.data.get('detail'), 'You do not have permission to perform this action.')






	" 										NO STAFF USER 										"

	def test_getting_answer_list_as_no_staff(self):
		answer_false = self.create_staff_answer()
		self.no_staff_user()
		answer = Answer.objects.all().first()
		url_get = reverse('answer:admin-list')

		response_answer_get = self.client.get(url_get,  format='json')
		# print (response_answer_get.data)
		self.assertEqual(response_answer_get.status_code, status.HTTP_403_FORBIDDEN)
		self.assertEqual(response_answer_get.data.get('detail'), 'You do not have permission to perform this action.')

	def test_getting_answer_detail_as_no_staff(self):
		answer_false = self.create_staff_answer()
		self.no_staff_user()
		answer = Answer.objects.all().first()
		url_get = reverse('answer:admin-detail', kwargs={'id': answer.id})

		response_answer_get = self.client.get(url_get,  format='json')
		# print (response_answer_get.data)
		self.assertEqual(response_answer_get.status_code, status.HTTP_403_FORBIDDEN)
		self.assertEqual(response_answer_get.data.get('detail'), 'You do not have permission to perform this action.')




