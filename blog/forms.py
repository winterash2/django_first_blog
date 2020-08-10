from django import forms
from .models import Post, Comment


def min_length_3_validator(value):
    if len(value) < 3:
        raise forms.ValidationError("3글자 이상 입력해주세요.")


class PostForm(forms.Form):
    title = forms.CharField(validators=[min_length_3_validator])
    text = forms.CharField(widget=forms.Textarea)


class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text',) #tuple 형태


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text',)
