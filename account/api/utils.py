import datetime
from django.conf import settings
from django.utils import timezone

from rest_framework_jwt.settings import api_settings

expire_delta = settings.JWT_AUTH['JWT_REFRESH_EXPIRATION_DELTA']


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': user.username,   #replace with UserSerializer
        'expires': timezone.now() + expire_delta
    }