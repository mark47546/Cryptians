from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
class Post(models.Model):
    title = models.CharField(max_length=100)
    coverImage = models.ImageField(upload_to='Post/', null=True,blank=True)
    body = HTMLField(null=True, blank=True)
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
    body = HTMLField(null=True, blank=True)

    posted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.post.title + ' | ' + self.body + ' By : ' + self.posted_by.username 