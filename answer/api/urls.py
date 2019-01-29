from django.urls import path
from .views import AnswerListAPIView, AnswerDetailAPIView, UserAnswerListAPIView, UserAnswerDetailAPIView, UserLoggedAnswerListAPIView

urlpatterns = [
    path('correct/', AnswerListAPIView.as_view()), # http://127.0.0.1:8000/api/answer/correct/
    path('correct/<id>/', AnswerDetailAPIView.as_view()),

    path('list/', UserLoggedAnswerListAPIView.as_view()),  # http://127.0.0.1:8000/api/answer/by_shell_second8/
    path('<user>/', UserAnswerListAPIView.as_view()),   # http://127.0.0.1:8000/api/answer/by_shell_second8/
    path('<user>/<id>/', UserAnswerDetailAPIView.as_view()),

]