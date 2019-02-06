from django.contrib.auth import authenticate, get_user_model
from django.db.models import Q
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserLoginSerializer, UserRegisterSerializer
from account.models import MyUser


from .permissions import IsAnonymous, IsStaffUser
# from .serializers import UserRegisterSerializer
from rest_framework_jwt.settings import api_settings

jwt_payload_handler             = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler              = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler    = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER



User = get_user_model()




# class AuthAPIView(APIView):
# 	serializer_class		= UserLoginSerializer




class AuthAPIView(APIView):
	permission_classes 		= [IsAnonymous]
	authentication_classes 	= []
	serializer_class 		= UserLoginSerializer

	def post(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return Response({'detail': 'You are already logged'}, status=400)
		data = request.data
		username = data.get('username')
		password = data.get('password')
		qs = User.objects.filter(
			Q(username__iexact=username) |
			Q(email__iexact=username)
		).distinct()
		if qs.count() == 1:
			user = qs.first()
			if user.check_password(password):
				payload = jwt_payload_handler(user)
				token = jwt_encode_handler(payload)
				my_payload = jwt_response_payload_handler(token, user, request=request)

				return Response(my_payload)
			else:
				return Response({'detail': 'Invalid credential'}, status=401)
		else:
			return Response({'detail': 'Invalid credential'}, status=401)



# class AuthAPIView(APIView):
# 	permission_classes 		= [permissions.AllowAny]
# 	authentication_classes 	= []
# 	serializer_class = UserLoginSerializer
#
# 	def post(self, request, *args, **kwargs):
# 		if request.user.is_authenticated:
# 			return Response({'detail': 'You are already logged'}, status=400)
# 		print (request.user)
# 		data = request.data
# 		username = data.get('username')
# 		password = data.get('password')
# 		qs = User.objects.filter(
# 			Q(username__iexact=username) |
# 			Q(email__iexact=username)
# 		).distinct()
# 		if qs.count() == 1:
# 			user = qs.first()
# 			if user.check_password(password):
# 				payload = jwt_payload_handler(user)
# 				token = jwt_encode_handler(payload)
# 				my_payload = jwt_response_payload_handler(token, user, request=request)
# 				return Response(my_payload)
# 			else:
# 				return Response({'detail': 'Invalid credential'}, status=401)
# 		else:
# 			return Response({'detail': 'Invalid credential'}, status=401)

class RegisterAPIView(generics.CreateAPIView):
	permission_classes 		= [IsAnonymous]
	serializer_class 		= UserRegisterSerializer
	queryset 				= User.objects.all()

	# def post(self, request, *args, **kwargs):
	# 	if request.user.is_authenticated:
	# 		return Response({'detail': 'You cannot reqister while you are logged'})
	# 	else:
	# 		data = request.data


# class RegisterAPIView(APIView):
# 	permission_classes 		= [permissions.AllowAny]
#
# 	def post(self, request, *args, **kwargs):
# 		if request.user.is_authenticated:
# 			return Response({'detail': 'You cannot reqister while you are logged'})
# 		else:
# 			data = request.data
# 			print(data)
# 			username = data.get('username')
# 			email = data.get('email')
# 			password = data.get('password')
# 			confirm_password = data.get('confirm_password')
# 		qs = User.objects.filter(
# 			Q(username__iexact=username) |
# 			Q(email__iexact=email)
# 		).distinct()
# 		print (qs.exists())
# 		if qs.exists():
# 			return Response({'detail':'User already exists.'}, status=401)
# 		else:
# 			print(password)
# 			if password != confirm_password:
# 				return Response({'detail':'Passwords must match'}, status=401)
# 			else:
# 				user = User.objects.create(
# 					username = username,
# 					email = email,
# 				)
# 				user.set_password(password)
# 				user.save()
# 				payload = jwt_payload_handler(user)
# 				token = jwt_encode_handler(payload)
# 				my_payload = jwt_response_payload_handler(token, user, request=request)
# 				return Response(my_payload, status=201)




# class AuthAPIView(APIView):
#     permission_classes = []
#     authentication_classes = []
#
#     def post(self, request, *args, **kwargs):
#         # print(request.user)
#         if request.user.is_authenticated():
#             return Response({'detail': 'You are already authenticated'}, status=400)
#         data = request.data
#         username = data.get('username')  # username or email address
#         password = data.get('password')
#         qs = User.objects.filter(
#             Q(username__iexact=username) |
#             Q(email__iexact=username)
#         ).distinct()
#         if qs.count() == 1:
#             user_obj = qs.first()
#             if user_obj.check_password(password):
#                 user = user_obj
#                 payload = jwt_payload_handler(user)
#                 token = jwt_encode_handler(payload)
#                 response = jwt_response_payload_handler(token, user, request=request)
#                 return Response(response)
#         return Response({"detail": "Invalid credentials"}, status=401)


# class RegisterAPIView(generics.CreateAPIView):
#     pass
#     queryset                = User.objects.all()
#     serializer_class        = UserRegisterSerializer
#     permission_classes      = []
#
#     def get_serializer_context(self, *args, **kwargs):
#         return {"request": self.request}




# class RegisterAPIView(APIView):
#     permission_classes      = [permissions.AllowAny]
#     def post(self, request, *args, **kwargs):
#         if request.user.is_authenticated():
#             return Response({'detail': 'You are already registered and are authenticated.'}, status=400)
#         data = request.data
#         username        = data.get('username') # username or email address
#         email           = data.get('username')
#         password        = data.get('password')
#         password2       = data.get('password2')
#         qs = User.objects.filter(
#                 Q(username__iexact=username)|
#                 Q(email__iexact=username)
#             )
#         if password != password2:
#             return Response({"password": "Password must match."}, status=401)
#         if qs.exists():
#             return Response({"detail": "This user already exists"}, status=401)
#         else:
#             user = User.objects.create(username=username, email=email)
#             user.set_password(password)
#             user.save()
#             # payload = jwt_payload_handler(user)
#             # token = jwt_encode_handler(payload)
#             # response = jwt_response_payload_handler(token, user, request=request)
#             # return Response(response, status=201)
#             return Response({'detail': "Thank you for registering. Please verify your email."}, status=201)
#         return Response({"detail": "Invalid Request"}, status=400)




