from django.conf.urls import url, include
from django.urls import path
from .views import QuestionListAPIView, QuestionDetailAPIView

urlpatterns = [
    path('', QuestionListAPIView.as_view()),
    path('<id>/', QuestionDetailAPIView.as_view()),

]
