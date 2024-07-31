from django.urls import path
from quizapp import views

urlpatterns = [
    path("", views.QuizListView.as_view(), name="quiz-list"),

    path("create/", views.QuizCreateView.as_view(), name="create-quiz"),

    path("<int:quiz_id>/question/create/", views.QuestionCreateView.as_view(), name="create-question"),
]
