from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from question.models import Question
from account.models import MyUser
# Create your models here.

class Answer(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='related_answer', verbose_name='question_id')
	answer_question = models.CharField(max_length=1000)
	is_correct = models.BooleanField(default=False)

	def __str__(self):
		return "{}: {} - {}".format(str(self.question),str(self.answer_question), str(self.is_correct))

	class Meta:
		ordering = ['question']


class UserGrade(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL,
								on_delete=models.CASCADE,
								related_name='related_grade',
								)
	grade = models.IntegerField(default=0)

	def __str__(self):
		return str(self.user)


class UserAnswer(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,
							 on_delete=models.CASCADE,
							 related_name='related_user',
							 )
	question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='related_user_answer')
	user_answer_id = models.SmallIntegerField()

	@property
	def owner(self):
		return self.user


def post_save_user_grade(instance, sender, created, *args, **kwargs):
	if created:
		UserGrade.objects.create(user=instance).save()

def post_save_user_grade_setter(instance, sender, created, *args, **kwargs):
	if created:
		total_correct_answers = 0
		qs = UserAnswer.objects.filter(user=instance.user)
		for item in qs:
			correct_answer = Answer.objects.filter(question=item.question, is_correct=True).first()
			if item.user_answer_id == correct_answer.id:
				total_correct_answers += correct_answer.question.rank
			else:
				continue
		user_grade = UserGrade.objects.get(user=instance.user)
		user_grade.grade = total_correct_answers
		user_grade.save()


post_save.connect(post_save_user_grade, sender=MyUser)
post_save.connect(post_save_user_grade_setter, sender=UserAnswer)