from django.db import models
from django.forms import ModelForm
from .models import Post, Comment



class CreatePostForm(ModelForm):
    class Meta:
        model = Post
        fields = "__all__"
        exclude = ["id"]

class UpdatePostForm(ModelForm):
    class Meta:
        model = Post
        fields = "__all__"
        exclude = ["id"]




class CreateCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = "__all__"
        exclude = ["id"]

class UpdateCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = "__all__"
        exclude = ["id"]
