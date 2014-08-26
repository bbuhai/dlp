from django.contrib import admin
from personalitytests.models import (Test, Score, Question, Answer)


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 2


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = ('question', 'test')


class ScoreInline(admin.TabularInline):
    model = Score
    extra = 2


class TestAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Test details', {'fields': ['name', 'description']})
    ]
    inlines = [ScoreInline]
    list_display = ('name', 'created_at')
    search_fields = ['name']


admin.site.register(Test, TestAdmin)
admin.site.register(Question, QuestionAdmin)