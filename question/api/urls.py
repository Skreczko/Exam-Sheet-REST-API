from django.conf.urls import url, include
from django.urls import path
from .views import QuestionListAPIView, QuestionDetailAPIView


app_name = 'question'

urlpatterns = [
    path('', QuestionListAPIView.as_view(), name='list'), # http://127.0.0.1:8000/api/question/
    path('<id>/', QuestionDetailAPIView.as_view(), name='detail'),

]
