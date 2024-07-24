from django import forms

from quizapp.models import Quiz, Question


class QuizCreate(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ["title", "description", "image"]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control mb-2'}),
            'description': forms.Textarea(attrs={'class': 'form-control mb-2'}),
            'image': forms.FileInput(attrs={"type": 'file', "class": 'form-control mb-2'})
        }

class QuestionCreate(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["title", "description", "image"]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control mb-2'}),
            'description': forms.Textarea(attrs={'class': 'form-control mb-2'}),
            'image': forms.FileInput(attrs={"type": 'file', "class": 'form-control mb-2'})
        }


