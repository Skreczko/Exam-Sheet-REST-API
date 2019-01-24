from django.contrib import admin
from .models import Question
# Register your models here.

class QuestionAdmin(admin.ModelAdmin):
	list_display = ['id','question','rank']
	list_filter = ['rank']
	search_fields = ['question']
	list_per_page = 50

	class Meta:
		model = Question


admin.site.register(Question, QuestionAdmin)