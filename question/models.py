from django.db import models

# Create your models here.

class Question(models.Model):
	question 	= models.CharField(max_length=1000)
	rank 		= models.PositiveSmallIntegerField(default=1)

	def __str__(self):
		return str(self.question) + (str(self.rank))