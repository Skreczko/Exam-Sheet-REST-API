from django.contrib import admin
from .models import Answer, UserAnswer
# Register your models here.

class AnswerAdmin(admin.ModelAdmin):
	list_display = ['id','question', 'answer_question', 'is_true']
	list_filter = ['question']
	list_per_page = 50

	class Meta:
		model = Answer

	def is_true(self, obj):
		if obj.is_correct:
			return True
		else:
			return False
	is_true.boolean = True



class UserAnswerAdmin(admin.ModelAdmin):
	list_display = ['id','user_id', 'user_name', 'question', 'user_answer_id', ]
	list_filter =['user_id']
	list_per_page = 50

	class Meta:
		model = UserAnswer

	def user_id(self, obj):
		return obj.user.id

	def user_name(self, obj):
		return obj.user


admin.site.register(Answer, AnswerAdmin)
admin.site.register(UserAnswer, UserAnswerAdmin)