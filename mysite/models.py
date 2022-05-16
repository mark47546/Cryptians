from email.policy import default
from django.db import models
from login.models import User
from taggit.managers import TaggableManager
from taggit.models import GenericUUIDTaggedItemBase, TaggedItemBase
from ckeditor.fields import RichTextField
from django_cryptography.fields import encrypt
from django.utils.translation import ugettext_lazy as _
import uuid

class UUIDTaggedItem(GenericUUIDTaggedItemBase, TaggedItemBase):
    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    coverImage = models.ImageField(upload_to='Post/', null=True,blank=True)
    body = encrypt(RichTextField(null=False, blank=False, default=""))
    tags = TaggableManager(through=UUIDTaggedItem, blank=False)
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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='PostComment')
    body = encrypt(RichTextField(null=False, blank=False, default=""))

    posted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.post.title + ' | ' + self.body + ' By : ' + self.posted_by.username 

class Tweet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tweet_id = models.CharField(max_length=250, null=True, blank=True)
    tweet_name = encrypt(models.CharField(max_length=250, null=True, blank=True))
    tweet_text = models.TextField()
    published_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.tweet_text
