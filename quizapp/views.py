from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from quizapp.forms import QuizCreate, QuestionCreate, AnswerFormSet
from quizapp.mixins import UserIsOwnerMixin, QuizCanEditMixin
from quizapp.models import Quiz, Question, QuizLive


# Create your views here.
class QuizListView(ListView):
    model = Quiz
    context_object_name = "quizes"
    template_name = "quizapp/index.html"

class UserQuizListView(LoginRequiredMixin, QuizListView):
    template_name = "quizapp/myquizlist.html"

    def get_queryset(self):
        queryset = super().get_queryset().filter(author=self.request.user)
        return queryset


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
        quiz_id = self.kwargs.get('quiz_id')
        data['quiz'] = get_object_or_404(Quiz, pk = quiz_id)
        if self.request.POST:
            data['answers'] = AnswerFormSet(self.request.POST)
        else:
            data['answers'] = AnswerFormSet()
        return data

    def form_valid(self, form):
        quiz_id = self.kwargs.get('quiz_id')
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


class QuestionUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = Question
    template_name = "quizapp/QuestionCreate_form.html"
    form_class = QuestionCreate
    def get_success_url(self):
        return reverse_lazy("create-question", kwargs={"quiz_id": self.object.quiz.pk})

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['quiz'] = self.object.quiz
        if self.request.POST:
            data['answers'] = AnswerFormSet(self.request.POST, instance=self.object)
        else:
            data['answers'] = AnswerFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        self.object = form.save()

        context = self.get_context_data()
        answers = context['answers']
        if answers.is_valid():
            answers.instance = self.object
            answers.save()
        else:
            self.render_to_response(self.get_context_data(form=form))
        return super().form_valid(form)


class QuestionDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = Question
    template_name = "quizapp/DeleteConfirmationForm.html"
    context_object_name = 'question'

    def get_success_url(self):
        return reverse_lazy("create-question", kwargs={"quiz_id": self.object.quiz.pk})


class QuizDeleteView(LoginRequiredMixin, QuizCanEditMixin, DeleteView):
    model = Quiz
    template_name = "quizapp/DeleteConfirmationForm.html"
    context_object_name = 'quiz'
    success_url = reverse_lazy("quiz-list")


class QuizDetailView(DetailView):
    model = Quiz
    template_name = "quizapp/quiz_detail.html"

class QuizLiveCreateView(LoginRequiredMixin, CreateView):
    model = QuizLive
    fields = []
    success_url = reverse_lazy('quiz-list')
    def form_valid(self, form):
        form.instance.quiz = get_object_or_404(Quiz, pk=self.kwargs["quiz-id"])
        form.instance.host = self.request.user
        form.instance.save()
        return super().form_valid(form)

