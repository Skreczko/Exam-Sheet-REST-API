from rest_framework import serializers
from rest_framework.reverse import reverse
from answer.models import Answer, UserAnswer
from account.models import MyUser
from question.models import Question
from account.api.serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class AnswerSerializer(serializers.ModelSerializer):
	answer_uri = serializers.SerializerMethodField(read_only=True)
	class Meta:
		model = Answer
		fields = [
			'id',
			'question',
			'answer_uri',
			'answer_question',
			'is_correct',
		]

	def get_answer_uri(self, obj):
		request = self.context.get('request')
		return reverse('api-answer:admin-detail', kwargs={'id': obj.id}, request=request)


class AnswerDetailSerializer(serializers.ModelSerializer):
	related_question = serializers.PrimaryKeyRelatedField(source='question.question', read_only=True)
	class Meta:
		model = Answer
		fields = [
			'id',
			'related_question',
			'answer_question',
			'is_correct',
		]


class QuestionAnswerSerializer(serializers.ModelSerializer):
	answer = serializers.SerializerMethodField(read_only=True)
	class Meta:
		model = Question
		fields = [
			'id',
			'question',
			'rank',
			'answer',
		]

	def get_answer(self, obj):
		request = self.context.get('request')
		qs = Answer.objects.filter(question=obj)
		return AnswerSerializer(qs, many=True, context={'request': request}).data

	def get_answer_uri(self, obj):
		request = self.context.get('request')
		return reverse("answer:admin-detail", kwargs={'id': obj.id}, request=request)


class AnswerForUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = Answer
		fields = [
			'id',
			'answer_question',
		]


class UserAnswerSerializer(serializers.ModelSerializer):
	user_answer_id = serializers.IntegerField()
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
		logged_user = self.context.get('logged_user')
		question = data.get('question', None)
		user_answer_id = data.get('user_answer_id', None)
		if not UserAnswer.objects.filter(question=question, user = logged_user).exists():
			avaible_answers = Answer.objects.filter(question=question)
			answ_ids=[]
			for x in avaible_answers:
				answ_ids.append(x.id)
			if user_answer_id in answ_ids:
				return data
			else:
				raise serializers.ValidationError('Answer is not available for this question.')
		else:
			raise serializers.ValidationError('You cannot add more than one answer per question.')

	def get_avaible_answer(self, obj):
		question = obj.question
		qs = Answer.objects.filter(question=question)
		return AnswerForUserSerializer(qs, many=True).data


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


class UserChosedAnswer2Serializer(serializers.HyperlinkedModelSerializer):
	user_answer_id = serializers.IntegerField()
	is_correct = serializers.SerializerMethodField(read_only=True)
	class Meta:
		model = UserAnswer
		fields = [
			'id',
			'user_answer_id',
			'is_correct',
		]

	def get_is_correct(self,obj):
		return Answer.objects.get(id=obj.user_answer_id).is_correct


class UserLoggedAnswerSerializer(serializers.ModelSerializer):
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

	def get_avaible_answers(self, obj):
		qs = obj.related_answer.all()
		return AnswerForUserSerializer(qs, many=True).data

	def get_user_answer(self, obj, ):
		request = self.context.get('request')
		user = request.user
		if user.is_staff:
			qs = UserAnswer.objects.filter(question=obj)
		else:
			qs = UserAnswer.objects.filter(user=user, question=obj)
		return UserChosedAnswerSerializer(qs, many=True, context={'request': request}).data


class UserLoggedAnswer2Serializer(serializers.ModelSerializer):
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

	def get_avaible_answers(self, obj):
		qs = obj.related_answer.all()
		return AnswerForUserSerializer(qs, many=True).data

	def get_user_answer(self, obj, ):
		request = self.context.get('request')
		user_id = self.context.get("user_id")
		qs = UserAnswer.objects.filter(user=user_id, question=obj)
		return UserChosedAnswer2Serializer(qs, many=True, context={'request': request}).data


class UserListSerializer(serializers.ModelSerializer):
	grade = serializers.SerializerMethodField(read_only=True)
	uri_answers = serializers.SerializerMethodField(read_only=True)
	class Meta:
		model = MyUser
		fields = [
			'id',
			'username',
			'email',
			'uri_answers',
			'grade',
		]

	def get_grade(self,obj):
		grade = obj.related_grade.grade
		all_points = Answer.objects.all().first().question.total_weighting()
		return str("{}/{}").format(grade, all_points)

	def get_uri_answers(self, obj):
		request = self.context.get('request')
		return reverse('api-user-grade', kwargs={'id':obj.id}, request=request)


class UserDetailSerializer(serializers.ModelSerializer):
	detail = serializers.SerializerMethodField(read_only=True)
	grade = serializers.SerializerMethodField(read_only=True)
	class Meta:
		model = MyUser
		fields = [
			'id',
			'username',
			'email',
			'detail',
			'grade',
		]

	def get_avaible_answers(self, obj):
		qs = obj.related_answer.all()
		return AnswerForUserSerializer(qs, many=True).data

	def get_detail(self, obj):
		request = self.context.get('request')
		user_id = self.context.get("user_id")
		qs = Question.objects.all()
		return UserLoggedAnswer2Serializer(qs, many=True, context={'request': request, 'user_id':user_id}).data

	def get_grade(self,obj):
		grade = obj.related_grade.grade
		all_points = Answer.objects.all().first().question.total_weighting()
		return str("{}/{}").format(grade,all_points)