from django.contrib import admin
from survey.models import (Survey, Question, Answer, Result, Page)
from django.db import models
from django.forms import Textarea


class ResultInLine(admin.TabularInline):
    model = Result
    extra = 2
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 70})}
    }


class PageInline(admin.TabularInline):
    model = Page
    extra = 2


class SurveyAdmin(admin.ModelAdmin):
    inlines = [PageInline, ResultInLine]
    fieldsets = [
        ('Survey details', {'fields': ['name', 'description']})
    ]
    list_display = ('name', 'created_at')
    search_fields = ['name']


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = ('question_text', 'page', 'position')
    search_fields = ['question_text']


admin.site.register(Survey, SurveyAdmin)
admin.site.register(Question, QuestionAdmin)