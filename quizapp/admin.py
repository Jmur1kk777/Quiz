from django.contrib import admin
from quizapp.models import Quiz, Question, Answer, QuizResult, QuestionResult, QuizLive

# Register your models here.
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(QuizResult)
admin.site.register(QuestionResult)
admin.site.register(QuizLive)