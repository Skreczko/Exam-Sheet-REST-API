from django.urls import path
from .views import AnswerListAPIView, AnswerDetailAPIView, UserAnswerListAPIView, UserAnswerDetailAPIView, UserLoggedAnswerListAPIView


app_name = 'answer'

urlpatterns = [
    path('admin/', AnswerListAPIView.as_view(), name='admin-list'), # http://127.0.0.1:8000/api/answer/admin/
    path('admin/<id>/', AnswerDetailAPIView.as_view(), name='admin-detail'),

    path('summary/', UserLoggedAnswerListAPIView.as_view(), name='list'),  # http://127.0.0.1:8000/api/answer/by_shell_second8/
    path('summary/<id>/', UserAnswerDetailAPIView.as_view(), name='detail'),



]