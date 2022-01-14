from django.db import models
from django.forms import ModelForm
from .models import Post, Comment



class CreatePostForm(ModelForm):
    class Meta:
        model = Post
        fields = "__all__"

class UpdatePostForm(ModelForm):
    class Meta:
        model = Post
        fields = "__all__"




class CreateCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = "__all__"

class UpdateCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = "__all__"
