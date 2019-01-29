from django.db import models
from django.conf import settings
from question.models import Question
# Create your models here.

class Answer(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='related_answer', verbose_name='question_id')
	answer_question = models.CharField(max_length=1000)
	is_correct = models.BooleanField(default=False)


	def __str__(self):
		return "{}: {} - {}".format(str(self.question),str(self.answer_question), str(self.is_correct))

	class Meta:
		ordering = ['question']

class UserAnswer(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,
							 on_delete=models.CASCADE,
							 # limit_choices_to={'is_staff':False}
							 )
	question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='related_user_answer')
	user_answer_id = models.SmallIntegerField()

@property
def owner(self):
	return self.user

