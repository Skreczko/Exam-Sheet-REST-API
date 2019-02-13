from rest_framework import generics, mixins, permissions
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from answer.models import Answer, UserAnswer
from question.models import Question
from .serializers import AnswerSerializer, UserAnswerSerializer, UserLoggedAnswerSerializer, UserDetailSerializer
from .permissions import IsOwner, IsOwnerNoStaff

from account.models import MyUser
from .serializers import UserListSerializer

class AnswerListAPIView(generics.ListCreateAPIView):
	permission_classes 		= [permissions.IsAdminUser]
	# authentication_classes 	= [SessionAuthentication]
	serializer_class 		= AnswerSerializer

	def get_queryset(self, *args, **kwargs):
		request = self.request
		return Answer.objects.all()


class AnswerDetailAPIView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.RetrieveAPIView):
	permission_classes 		= [permissions.IsAdminUser]
	# authentication_classes = [SessionAuthentication]
	# queryset = Answer.objects.all()
	serializer_class 		= AnswerSerializer
	lookup_field 			= 'id'

	def get_queryset(self, *args, **kwargs):
		return Answer.objects.all()

	def put(self, request, *args, **kwargs):
		return self.update(request, *args, **kwargs)

	def delete(self, request, *args, **kwargs):
		return self.destroy(request, *args, **kwargs)


class UserAnswerListAPIView(generics.ListCreateAPIView):
	permission_classes 		= [IsOwner]
	# authentication_classes 	= [SessionAuthentication]
	queryset = UserAnswer.objects.all()
	serializer_class = UserAnswerSerializer

	def get_queryset(self, *args, **kwargs):
		username = self.kwargs.get('user', None)
		if username is not None:
			return UserAnswer.objects.filter(user__username=username).order_by('question')
		return UserAnswer.objects.none()

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

class UserLoggedAnswerListAPIView(generics.ListCreateAPIView):
	permission_classes 		= [IsOwnerNoStaff]
	queryset = Question.objects.all()
	serializer_class = None
	search_fields = ('question', 'user__username')
	ordering_fields = ('question', 'user__username', 'rank')

	def get_serializer_class(self):
		if self.request.method == 'POST':
			return UserAnswerSerializer
		elif self.request.method == 'GET':
			return UserLoggedAnswerSerializer

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)


class UserAnswerDetailAPIView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.RetrieveAPIView):
	permission_classes = [IsOwner]
	# authentication_classes = []
	queryset = UserAnswer.objects.all()
	serializer_class = UserAnswerSerializer
	lookup_field = 'id'

	def put(self, request, *args, **kwargs):
		return self.update(request, *args, **kwargs)

	def delete(self, request, *args, **kwargs):
		return self.destroy(request, *args, **kwargs)




class UserListGradeAPIView(generics.ListAPIView):
	permission_classes = []
	queryset = None
	serializer_class = UserListSerializer
	search_fields = ('username',)
	ordering_fields = ('username', 'email', 'related_grade__grade')

	def get_queryset(self):
		if self.request.user.is_staff:
			return MyUser.objects.all()
		else:
			if self.request.user.is_authenticated:
				return MyUser.objects.filter(username=self.request.user)
			else:
				return MyUser.objects.none()





class UserDetailGradeAPIView(generics.RetrieveAPIView):
	permission_classes = []
	queryset = None
	serializer_class = UserDetailSerializer
	lookup_field = 'id'

	def get_serializer_context(self):
		return {"user_id": self.kwargs.get('id')}

	def get_queryset(self):
		if self.request.user.is_staff:
			return MyUser.objects.all()
		else:
			if self.request.user.is_authenticated:
				return MyUser.objects.filter(username=self.request.user)
			else:
				return MyUser.objects.none()
