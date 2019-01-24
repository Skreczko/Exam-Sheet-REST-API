from rest_framework import serializers

from question.models import Question

class QuestionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Question
		fields = [
			'id',
			'user',
			'question',
			'rank'
		]

		read_only_fields = ['user']

	def validate_question(self, value):
		if str(value)[-1] != '?':
			raise serializers.ValidationError("Please add '?' to your question.")
		else:
			return value