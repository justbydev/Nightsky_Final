from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):

    Ch=(('1', '별'), ('2', '먹구름'),)
    emotion=forms.ChoiceField(choices=Ch, widget=forms.RadioSelect)
    
    class Meta:
        model = Post
        fields=['body', 'emotion',]

"""
class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['content',]
"""

class CommentForm(forms.ModelForm):
    #text = forms.TextInput(label = '댓글')

    class Meta:
        model = Comment
        fields = ['content']