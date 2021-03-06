from django import forms
from main.models import Comment, Answer

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'content']

        widgets = {
            'subject' : forms.TextInput(attrs={'class':'form-control'}),
            'content' : forms.Textarea(attrs={'class': 'form-control', 'rows': 10})
        }
        labels = {
            'subject':'제목',
            'content': '내용',
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
        'content': '답변내용',
        }