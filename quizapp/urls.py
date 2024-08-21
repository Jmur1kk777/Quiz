from django.urls import path
from quizapp import views

urlpatterns = [
    path("", views.QuizListView.as_view(), name="quiz-list"),
    path("my-quizzes/", views.UserQuizListView.as_view(), name="user-quiz-list"),

    path("create/", views.QuizCreateView.as_view(), name="create-quiz"),

    path("<int:quiz_id>/question/create/", views.QuestionCreateView.as_view(), name="create-question"),
    path("question/<int:pk>/update/", views.QuestionUpdateView.as_view(), name="update-question"),
    path("question/<int:pk>/delete/", views.QuestionDeleteView.as_view(), name="delete-question"),
    path("quiz/<int:pk>/delete/", views.QuizDeleteView.as_view(), name="delete-quiz"),
    path("quiz/<int:pk>/live/create/", views.QuizLiveCreateView.as_view(), name="create-quiz-live"),
]
