from django.db import models
from django.conf import settings
# Create your models here.

RANKS = tuple((x,x) for x in range(1,4))

class Question(models.Model):
	user 		= models.ForeignKey(settings.AUTH_USER_MODEL,
									on_delete=models.CASCADE,
									limit_choices_to={'is_staff': True},
									)
	question 	= models.CharField(max_length=1000)
	rank 		= models.PositiveSmallIntegerField(default=1, choices=RANKS)

	def __str__(self):
		return str(self.question)


