from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from quizapp.forms import QuizCreate
from quizapp.models import Quiz


# Create your views here.
class QuizListView(ListView):
    model = Quiz
    context_object_name = "quizes"
    template_name = "quizapp/index.html"
    paginate_by = 10

class QuizCreateView(LoginRequiredMixin, CreateView):
    model = Quiz
    template_name = "quizapp/QuizCreate_form.html"
    form_class = QuizCreate
    success_url = reverse_lazy("quiz-list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

