from rest_framework import serializers
from django.conf import settings
from answer.models import Answer, UserAnswer

class AnswerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Answer
		fields = [
			'id',
			'question',
			'question_answer',
			'is_correct',
		]


class UserAnswerSerializer(serializers.ModelSerializer):
	user_answer_id = serializers.IntegerField()
	class Meta:
		model = UserAnswer
		fields = [
			'id',
			'user',
			'question',
			'user_answer_id',
		]
	def validate(self, data):
		question = data.get('question', None)
		user_answer_id = data.get('user_answer_id', None)
		avaible_answers = question.related_answer.all()
		answ_ids=[]
		for x in avaible_answers:
			answ_ids.append(x.id)
		if user_answer_id in answ_ids:
			return data
		else:
			raise serializers.ValidationError('Answer is not available for this question.')