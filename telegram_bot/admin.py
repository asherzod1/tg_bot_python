from django.contrib import admin

from telegram_bot.models import Question, Answer


# Register your models here.

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text')
    list_display_links = ('id', )


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'question', 'text')
    list_display_links = ('id', )