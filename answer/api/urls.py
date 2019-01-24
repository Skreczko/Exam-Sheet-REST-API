from django.urls import path
from .views import AnswerListAPIView, AnswerDetailAPIView, UserAnswerListAPIView, UserAnswerDetailAPIView

urlpatterns = [
    path('correct/', AnswerListAPIView.as_view()),
    path('correct/<id>/', AnswerDetailAPIView.as_view()),
    path('<user>/', UserAnswerListAPIView.as_view()),
    path('<user>/<id>/', UserAnswerDetailAPIView.as_view()),

]