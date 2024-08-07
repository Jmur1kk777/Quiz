from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from quizapp.forms import QuizCreate, QuestionCreate, AnswerFormSet
from quizapp.models import Quiz, Question


# Create your views here.
class QuizListView(ListView):
    model = Quiz
    context_object_name = "quizes"
    template_name = "quizapp/index.html"



class QuizCreateView(LoginRequiredMixin, CreateView):
    model = Quiz
    template_name = "quizapp/QuizCreate_form.html"
    form_class = QuizCreate
    success_url = reverse_lazy("quiz-list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("create-question", kwargs={"quiz_id": self.object.pk})


class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    template_name = "quizapp/QuestionCreate_form.html"
    form_class = QuestionCreate
    def get_success_url(self):
        return reverse_lazy("create-question", kwargs={"quiz_id": self.object.quiz.pk})

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['answers'] = AnswerFormSet(self.request.POST)
        else:
            data['answers'] = AnswerFormSet()
        return data

    def form_valid(self, form):
        quiz_id = self.kwargs['quiz_id']
        quiz = get_object_or_404(Quiz, id=quiz_id)
        form.instance.author = self.request.user
        form.instance.quiz = quiz
        self.object = form.save()

        context = self.get_context_data()
        answers = context['answers']
        if answers.is_valid():
            answers.instance = self.object
            answers.save()
        else:
            self.render_to_response(self.get_context_data(form=form))
        return super().form_valid(form)
