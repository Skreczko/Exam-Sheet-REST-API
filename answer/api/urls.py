from django.urls import path
from .views import AnswerListAPIView, AnswerDetailAPIView, UserAnswerListAPIView, UserAnswerDetailAPIView, UserLoggedAnswerListAPIView


app_name = 'answer'

urlpatterns = [
    path('admin/', AnswerListAPIView.as_view()), # http://127.0.0.1:8000/api/answer/correct/
    path('admin/<id>/', AnswerDetailAPIView.as_view()),

    path('summary/', UserLoggedAnswerListAPIView.as_view()),  # http://127.0.0.1:8000/api/answer/by_shell_second8/
    path('summary/<id>/', UserAnswerDetailAPIView.as_view(), name='detail'),
    # path('<user>/', UserAnswerListAPIView.as_view()),   # http://127.0.0.1:8000/api/answer/by_shell_second8/


]