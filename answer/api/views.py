from rest_framework import generics, mixins, permissions
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from answer.models import Answer, UserAnswer
from question.models import Question
from .serializers import AnswerSerializer, UserAnswerSerializer, UserLoggedAnswerSerializer
from .permissions import IsOwner, IsStaffUser


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
		request = self.request
		print(request.user)
		print('loool')
		return Answer.objects.all()

	def patch(self, request, *args, **kwargs):
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

class UserLoggedAnswerListAPIView(generics.ListAPIView):
	permission_classes 		= [IsOwner]
	# authentication_classes 	= [SessionAuthentication]
	queryset = Question.objects.all()
	serializer_class = UserLoggedAnswerSerializer

	# def get_queryset(self, *args, **kwargs):
	# 	username = self.kwargs.get('user', None)
	# 	if username is not None:
	# 		return UserAnswer.objects.filter(user__username=username).order_by('question')
	# 	return UserAnswer.objects.none()
	#
	# def perform_create(self, serializer):
	# 	serializer.save(user=self.request.user)


class UserAnswerDetailAPIView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.RetrieveAPIView):
	permission_classes = [IsOwner]
	# authentication_classes = []
	queryset = UserAnswer.objects.all()
	serializer_class = UserAnswerSerializer
	lookup_field = 'id'



	def put(self, request, *args, **kwargs):
		return self.update(request, *args, **kwargs)

	#
	# def post(self, request, *args, **kwargs):
	# 	return self.create(request, *args, **kwargs)

	def delete(self, request, *args, **kwargs):
		return self.destroy(request, *args, **kwargs)



from rest_framework.views import APIView

class UserAnsweAddAPIView(APIView):
	permission_classes 		= [IsOwner]
	# authentication_classes 	= [SessionAuthentication]


	def get(self, request, format=None):
		qs = Question.objects.all()
		user = self.request.user
		print(qs)

		serializer = UserLoggedAnswerSerializer(qs, many=True)
		print(serializer.data)
		return Response(serializer.data)

	def post(self, request, format=None):
		pass

	# def post(self, request, *args, **kwargs):
	# 	data = request.data
	# 	username = data.get('username')
	# 	password = data.get('password')
	# 	qs = User.objects.filter(
	# 		Q(username__iexact=username) |
	# 		Q(email__iexact=username)
	# 	).distinct()
	# 	if qs.count() == 1:
	# 		user = qs.first()
	# 		if user.check_password(password):
	# 			payload = jwt_payload_handler(user)
	# 			token = jwt_encode_handler(payload)
	# 			my_payload = jwt_response_payload_handler(token, user, request=request)
	#
	# 			return Response(my_payload)
	# 		else:
	# 			return Response({'detail': 'Invalid credential'}, status=401)
	# 	else:
	# 		return Response({'detail': 'Invalid credential'}, status=401)

