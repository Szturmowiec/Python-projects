from django.contrib import admin
from .models import Question, Choice, ReportQuestion, Profile

class ChoiceInline(admin.StackedInline):
    model=Choice
    fieldsets = [
        (None,{'fields': ['choice_text']}),
    ]
    extra=1

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]

class ReportQuestionAdmin(admin.ModelAdmin):
    model=ReportQuestion
    fieldsets=[
        (None,{'fields': ['question']}),
    ]

admin.site.register(Question,QuestionAdmin)
admin.site.register(ReportQuestion,ReportQuestionAdmin)
admin.site.register(Profile)