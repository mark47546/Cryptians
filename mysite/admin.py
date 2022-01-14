from django.contrib import admin
from .models import Post, Comment
from django.db import models
from tinymce.widgets import TinyMCE

class textEditorAdmin(admin.ModelAdmin):

   list_display = ["content"]

   formfield_overrides = {

   models.TextField: {'widget': TinyMCE()}

   }
   
admin.site.register(Post)
admin.site.register(Comment)

