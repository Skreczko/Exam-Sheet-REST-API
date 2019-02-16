from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from question.models import Question
from answer.models import Answer, UserAnswer
from rest_framework import status
from rest_framework.authtoken.models import Token

from django.contrib.auth import get_user_model

User = get_user_model()

class AnswerStaffAPITestCase(APITestCase):

	def staff_user(self):
		staff_user = User.objects.create(
			username	='StaffUser',
			email		='StaffUser@gmail.com',
			is_staff	=True,
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

	def no_staff_user(self, nickname='NoStaffUser'):
		no_staff_user = User.objects.create(
			username	= nickname,
			email		='{}@gmail.com'.format(nickname),
			is_staff	=False,
		)
		no_staff_user.set_password('OtherPassword1')
		no_staff_user.save()

		url_login = reverse('account:login')
		data_login = {
			'username'	: nickname,
			'password'	: 'OtherPassword1',
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
		data_answer1_false = {
			"question"			: question,
			"answer_question"	: "Incorrect answer",
			"is_correct"		: False,
		}
		data_answer2_true = {
			"question"			: question,
			"answer_question"	: "This answer is true",
			"is_correct"		: True,
		}
		data_answer3_false = {
			"question"			: question,
			"answer_question"	: "Second incorrect answer",
			"is_correct"		: False,
		}
		self.client.post(url_answer, data_answer2_true, format='json')
		self.client.post(url_answer, data_answer3_false, format='json')
		return self.client.post(url_answer, data_answer1_false, format='json')

	def test_creating_answer_success(self):
		answer_false = self.create_staff_answer()
		question = Question.objects.all().first().id

		self.assertEqual(Answer.objects.all().count(), 3)
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
		self.assertEqual(Answer.objects.all().count(), 2)

	def test_getting_UserAnswer_list_as_no_staff_failed(self):
		answer_false = self.create_staff_answer()
		answer = Answer.objects.all().first()
		url_update = reverse('answer:list')

		response_answer_get = self.client.get(url_update,  format='json')
		# print (response_answer_get.data)
		self.assertEqual(response_answer_get.status_code, status.HTTP_403_FORBIDDEN)
		self.assertEqual(response_answer_get.data.get('detail'), 'You do not have permission to perform this action.')




	" 										NO STAFF USER 										"


	def test_getting_answer_list_as_no_staff_failed(self):
		answer_false = self.create_staff_answer()
		self.no_staff_user()
		answer = Answer.objects.all().first()
		url_get = reverse('answer:admin-list')

		response_answer_get = self.client.get(url_get,  format='json')
		# print (response_answer_get.data)
		self.assertEqual(response_answer_get.status_code, status.HTTP_403_FORBIDDEN)
		self.assertEqual(response_answer_get.data.get('detail'), 'You do not have permission to perform this action.')

	def test_getting_answer_detail_as_no_staff_failed(self):
		answer_false = self.create_staff_answer()
		self.no_staff_user()
		answer = Answer.objects.all().first()
		url_get = reverse('answer:admin-detail', kwargs={'id': answer.id})

		response_answer_get = self.client.get(url_get,  format='json')
		# print (response_answer_get.data)
		self.assertEqual(response_answer_get.status_code, status.HTTP_403_FORBIDDEN)
		self.assertEqual(response_answer_get.data.get('detail'), 'You do not have permission to perform this action.')

	def user_answer_create(self):
		self.create_staff_answer()
		self.no_staff_user()
		question = Question.objects.all().first()
		url_user_answer = reverse('answer:list')

		data_user_answer_create = {
			'question'			: question.id,
			'user_answer_id'	: 3,
		}
		return self.client.post(url_user_answer, data_user_answer_create, format='json')

	def test_creating_user_answer_success(self):
		response_answer_create = self.user_answer_create()
		# print(response_answer_create.data)
		self.assertEqual(response_answer_create.status_code, status.HTTP_201_CREATED)
		self.assertEqual(UserAnswer.objects.all().exists(), True)

	def test_creating_second_user_answer_success(self):
		self.user_answer_create()						#creating question + add related answers for question + add user answer
		self.no_staff_user(nickname="OtherNoStaff")	#login as second non staff user + add user answer
		question = Question.objects.all().first()
		url_user_answer = reverse('answer:list')

		data_second_user_answer_create = {
			'question'			: question.id,
			'user_answer_id'	: 2,
		}
		response_answer_create_second_user = self.client.post(url_user_answer, data_second_user_answer_create, format='json')
		self.assertEqual(response_answer_create_second_user.status_code, status.HTTP_201_CREATED)
		self.assertEqual(UserAnswer.objects.all().count(), 2)
		self.assertNotEqual(UserAnswer.objects.all().first().user, UserAnswer.objects.all().last().user)

	def test_get_list_of_user_answers_for_question(self):
		self.user_answer_create()						#creating question + add related answers for question + add user answer
		self.no_staff_user(nickname="OtherNoStaff")	#login as second non staff user + add user answer
		question = Question.objects.all().first()
		url_user_answer = reverse('answer:list')
		data_second_user_answer_create = {
			'question'			: question.id,
			'user_answer_id'	: 2,
		}
		self.client.post(url_user_answer, data_second_user_answer_create, format='json')

		response_show_list = self.client.get(url_user_answer, format='json')
		self.assertEqual(response_show_list.data['results'][0]['user_answer'][0]['user']['username'], 'OtherNoStaff')


	def test_creating_user_second_answer_failed(self):
		self.user_answer_create()
		question = Question.objects.all().first()
		url_user_answer = reverse('answer:list')
		data_user_answer_create = {
			'question'			: question.id,
			'user_answer_id'	: 2,
		}
		response_answer_create_failed = self.client.post(url_user_answer, data_user_answer_create, format='json')
		# print(response_answer_create_failed.data)
		self.assertEqual(response_answer_create_failed.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(response_answer_create_failed.data.get('non_field_errors')[0], 'You cannot add more than one answer per question.')

	def test_creating_user_answer_failed(self):
		self.create_question()
		self.no_staff_user(nickname="OtherNoStaff")
		question = Question.objects.all().first()
		url_user_answer = reverse('answer:list')
		data_user_answer_create = {
			'question'			: question.id,
			'user_answer_id'	: 100,
		}
		response_answer_create_failed = self.client.post(url_user_answer, data_user_answer_create, format='json')
		# print(response_answer_create_failed.data)
		self.assertEqual(response_answer_create_failed.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(response_answer_create_failed.data.get('non_field_errors')[0], 'Answer is not available for this question.')

	def test_updating_user_answer_success(self):
		self.user_answer_create()
		question = Question.objects.all().first()
		user_answer = UserAnswer.objects.get(user__username='NoStaffUser')
		url_user_answer = reverse('answer:detail', kwargs={'id':user_answer.id})
		data_user_answer_update = {
			'question'			: question.id,
			'user_answer_id'	: 1,
		}
		response_edit = self.client.put(url_user_answer, data_user_answer_update, format='json')
		self.assertEqual(response_edit.status_code, status.HTTP_200_OK)

	def test_deleting_user_answer_success(self):
		self.user_answer_create()
		user_answer = UserAnswer.objects.get(user__username='NoStaffUser')
		url_user_answer = reverse('answer:detail', kwargs={'id':user_answer.id})

		response_delete = self.client.delete(url_user_answer, format='json')
		self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)
		self.assertEqual(UserAnswer.objects.filter(user__username='NoStaffUser').exists(), False)











