from rest_framework import generics, mixins, permissions
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication

from question.models import Question
from .serializers import QuestionSerializer
from answer.api.serializers import UserAnswerSerializer
from answer.api.permissions import IsStaffUser

class QuestionListAPIView(generics.ListCreateAPIView):
	permission_classes 		= [IsStaffUser]
	# authentication_classes 	= [SessionAuthentication]
	queryset 				= Question.objects.all()
	serializer_class 		= QuestionSerializer
	search_fields = ('question',)
	ordering_fields = ('rank', 'question',)

	def get_queryset(self):
		request = self.request
		qs = Question.objects.all()
		query = self.request.GET.get('q', None)
		if query:
			qs = qs.filter(question__icontains=query)
		return qs


	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

# class QuestionCreateAPIView(generics.CreateAPIView):
# 	permission_classes = []
# 	authentication_classes = []
# 	queryset = Question.objects.all()
# 	serializer_class = QuestionSerializer
#
# 	def perform_create(self, serializer):
# 		serializer.save(user=self.request.user)

class QuestionDetailAPIView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.RetrieveAPIView):
	permission_classes = [IsStaffUser]
	#authentication_classes = []
	queryset = Question.objects.all()
	serializer_class = QuestionSerializer
	lookup_field = 'id'

	def put(self, request, *args, **kwargs):
		return self.update(request, *args, **kwargs)


	def delete(self, request, *args, **kwargs):
		return self.destroy(request, *args, **kwargs)



