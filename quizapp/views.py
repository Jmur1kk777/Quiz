from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from quizapp.forms import QuizCreate, QuestionCreate, AnswerFormSet, QuizJoinForm, QuizAnswerForm
from quizapp.mixins import UserIsOwnerMixin, QuizCanEditMixin
from quizapp.models import Quiz, Question, QuizLive, QuizResult, QuestionResult


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
        self.object = form.save(commit=False)

        context = self.get_context_data()
        answers = context['answers']
        if answers.is_valid() and answers.cleaned_data:
            if not any(answer.cleaned_data.get('is_correct') for answer in answers):
                form.add_error(None, "Choose correct answer")
                return self.render_to_response(self.get_context_data(form=form))
            self.object.save()
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
        self.object = form.save(commit=False)

        context = self.get_context_data()
        answers = context['answers']
        if answers.is_valid() and answers.cleaned_data:
            if not any(answer.cleaned_data.get('is_correct') for answer in answers):
                form.add_error(None, "Choose correct answer")
                return self.render_to_response(self.get_context_data(form=form))
            self.object.save()
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
    context_object_name = 'quiz'


class QuizLiveCreateView(LoginRequiredMixin, CreateView):
    model = QuizLive
    fields = []

    def get_success_url(self):
        return reverse_lazy("quiz-live-detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        form.instance.quiz = get_object_or_404(Quiz, pk=self.kwargs["pk"])
        form.instance.host = self.request.user
        form.instance.save()
        return super().form_valid(form)


class QuizLiveDetailView(LoginRequiredMixin, DetailView):
    model = QuizLive
    context_object_name = 'live_quiz'
    template_name = "quizapp/quiz_live.html"


class QuizJoinView(LoginRequiredMixin, CreateView):
    model = QuizResult
    template_name = "quizapp/quiz_join.html"
    form_class = QuizJoinForm

    def form_valid(self, form):
        form.instance.quiz_live = get_object_or_404(QuizLive, invite_code=self.kwargs["invite_code"])
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
        form.instance.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("quiz-live-answer", kwargs={"quiz_result_id": self.object.pk})

def answer_question(request, quiz_result_id):
    quiz_result  = get_object_or_404(QuizResult, id = quiz_result_id)
    responses = quiz_result.responses.values_list('question', flat=True)
    question = quiz_result.quiz_live.quiz.questions.exclude(id__in=responses).first()
    if request.method == 'POST':
        form = QuizAnswerForm(request.POST, question=question)
        if form.is_valid():
            answer = form.cleaned_data['answer']
            score = 10 if answer.is_correct else 0

            QuestionResult.objects.create(quiz_result=quiz_result, question=question, answer=answer, score=score)
            quiz_result.score += score
            quiz_result.save()

            next_question = quiz_result.quiz_live.quiz.questions.exclude(id__in=responses).first()
            if next_question:
                return redirect(reverse_lazy("quiz-live-answer", kwargs={"quiz_result_id": quiz_result.pk}))
            else:
                quiz_result.completed = True
                quiz_result.save()
                return redirect(reverse_lazy("quiz-live-detail", kwargs={"pk": quiz_result.quiz_live.pk}))

    else:
        form = QuizAnswerForm(question=question)
    context = {
        'quiz_result': quiz_result,
        'question': question,
        'form': form
    }

    return render(request, "quizapp/answer_question.html",context)