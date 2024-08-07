from django import forms

from quizapp.models import Quiz, Question, Answer


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
        fields = ["text", "type", "image", "video", "time_limit"]

    def __init__(self, *args, **kwargs):
        super(QuestionCreate, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control mb-2', })


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ["text", "is_correct"]

    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field == "is_correct":
                self.fields[field].widget.attrs.update({'class': 'form-check-input mb-2',})
            else:
                self.fields[field].widget.attrs.update({'class': 'form-control mb-2', 'rows':'3' })

AnswerFormSet = forms.inlineformset_factory(Question, Answer, form=AnswerForm,extra=4)
