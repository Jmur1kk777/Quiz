from django import forms

from quizapp.models import Quiz


class QuizCreate(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ["title", "description", "image"]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control mb-2'}),
            'description': forms.Textarea(attrs={'class': 'form-control mb-2'}),
            'image': forms.FileInput(attrs={"type": 'file', "class": 'form-control mb-2'})
        }
