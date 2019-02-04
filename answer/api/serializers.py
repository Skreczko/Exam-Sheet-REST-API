from rest_framework import serializers
from rest_framework.reverse import reverse
from django.conf import settings
from answer.models import Answer, UserAnswer
from question.api.serializers import QuestionReadOnlySerializer
from question.models import Question
from account.api.serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()
import json

class AnswerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Answer
		fields = [
			'id',
			'question',
			'answer_question',
			'is_correct',
		]

class AnswerForUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = Answer
		fields = [
			'id',
			# 'question',
			'answer_question',
		]

	def get_uri(self,obj):
		return "/api/"

class UserAnswerSerializer(serializers.ModelSerializer):
	user_answer_id = serializers.IntegerField()
	# question = serializers.StringRelatedField(many=False)
	user = UserSerializer(many=False, read_only=True)
	avaible_answer = serializers.SerializerMethodField(read_only=True)


	class Meta:
		model = UserAnswer
		fields = [
			'id',
			'user',
			'question',
			'avaible_answer',
			'user_answer_id',

		]

		read_only_fields = ['user', 'avaible_answer',]


	def validate(self, data):
		question = data.get('question', None)
		# question = data.get('question', None)
		user_answer_id = data.get('user_answer_id', None)
		avaible_answers = Answer.objects.filter(question=question)
		print(avaible_answers)
		answ_ids=[]
		for x in avaible_answers:
			answ_ids.append(x.id)
		if user_answer_id in answ_ids:
			return data
		else:
			raise serializers.ValidationError('Answer is not available for this question.')


	def get_avaible_answer(self, obj):
		question = obj.question
		qs = Answer.objects.filter(question=question)
		return AnswerForUserSerializer(qs, many=True).data










"""
http://127.0.0.1:8000/api/answer/list/
"""

class UserChosedAnswerSerializer(serializers.HyperlinkedModelSerializer):
	user_answer_id = serializers.IntegerField()
	user = UserSerializer(User, many=False, read_only=True)
	uri = serializers.HyperlinkedIdentityField(view_name='answer:detail', read_only=True, lookup_field='id')

	class Meta:
		model = UserAnswer
		fields = [
			'id',
			'uri',
			'user_answer_id',
			'user',
		]

	def get_url(self, obj):
		request = self.context.get('request')
		return reverse('answer:detail', kwargs={'id': obj.id}, request=request)




class UserLoggedAnswerSerializer(serializers.ModelSerializer):
	# uri_question = serializers.SerializerMethodField(read_only=True)

	avaible_answers = serializers.SerializerMethodField(read_only=True)
	user_answer = serializers.SerializerMethodField(read_only=True)



	class Meta:
		model = Question
		fields = [
			'id',
			'rank',
			'question',
			'avaible_answers',
			'user_answer',
		]
#
# """
# to dodamy do admina jak cos
# 	def get_uri_question(self, obj):
# 		request = self.context.get('request')
# 		return reverse('question:detail', kwargs={'id': obj.id}, request=request)
#
# 	def get_uri_user_answer(self, obj):
# 		request = self.context.get('request')
# 		return reverse('answer:detail', kwargs={'id': obj.id}, request=request)
#
# """

	def get_avaible_answers(self, obj):
		qs = obj.related_answer.all()
		return AnswerForUserSerializer(qs, many=True).data

	# def get_user_answer(self, obj, ):
	# 	request = self.context.get('request')
	# 	qs = UserAnswer.objects.filter(question=obj,)
	# 	return UserChosedAnswerSerializer(qs, many=True, context={'request': request}).data

	def get_user_answer(self, obj, ):
		request = self.context.get('request')
		user = request.user
		qs = UserAnswer.objects.filter(user=user, question=obj)
		return UserChosedAnswerSerializer(qs, many=True, context={'request': request}).data











