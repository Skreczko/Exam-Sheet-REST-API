from rest_framework import serializers
from rest_framework.reverse import reverse
from question.models import Question


class QuestionSerializer(serializers.ModelSerializer):
	uri = serializers.SerializerMethodField(read_only=True)
	class Meta:
		model = Question
		fields = [
			'id',
			'uri',
			'user',
			'question',
			'rank'
		]

		read_only_fields = ['user']

	def get_uri(self, obj):
		request = self.context.get('request')
		return reverse('question:detail', kwargs={'id': obj.id}, request=request)

	def validate_question(self, value):
		if str(value)[-1] != '?':
			raise serializers.ValidationError("Please add '?' to your question.")
		else:
			return value


class QuestionReadOnlySerializer(serializers.ModelSerializer):
	class Meta:
		model = Question
		fields = [
			'id',
			'rank',
			'question',
			# 'avaible_answers'
		]
		read_only_field=['rank']

class QuestionReadOnlySerialize2(serializers.ModelSerializer):
	class Meta:
		model = Question
		fields = [
			'id',
			'rank',
			'question',
			# 'avaible_answers'
		]

