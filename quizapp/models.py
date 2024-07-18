from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Quiz(models.Model):
    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to="quiz_image", null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Question(models.Model):
    QUESTION_TYPES = [
        ("text","Text question"),
        ("image", "Image question"),
        ("video", "Video question")
    ]

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()
    type = models.CharField(max_length=20, choices=QUESTION_TYPES, default="text")
    image = models.ImageField(upload_to='question_images/',blank=True, null=True)
    video = models.FileField(upload_to='question_videos/',blank=True, null=True)
    created = models.DateField(auto_now_add=True)
    time_limit = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE,related_name="answers")
    text = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class QuizResult(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="results")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="results")
    score = models.IntegerField(default=0)
    completed_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.quiz


class QuestionResult(models.Model):
    quiz_result = models.ForeignKey(QuizResult, on_delete=models.CASCADE, related_name="responses")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="responses")
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE,)
    time = models.IntegerField(default=0)