from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField

class Post(models.Model):
    title = models.CharField(max_length=100)
    coverImage = models.ImageField(upload_to='Post/', null=True,blank=True)
    body = RichTextField(null=True, blank=True)
    tags = TaggableManager()
    posted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def delete(self, *args, **kwaegs):
        self.coverImage.delete()
        super().delete(*args, **kwaegs)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title + ' | ' + self.posted_by.username

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='PostComment')
    body = RichTextField(null=True, blank=True)

    posted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.post.title + ' | ' + self.body + ' By : ' + self.posted_by.username 

class Tweet(models.Model):
    tweet_id = models.CharField(max_length=250, null=True, blank=True)
    tweet_name = models.CharField(max_length=250, null=True, blank=True)
    tweet_text = models.TextField()
    published_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.tweet_text

    