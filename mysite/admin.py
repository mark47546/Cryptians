from django.contrib import admin
from .models import Post, Comment, Tweet

class excludeID(admin.ModelAdmin):
    exclude = ["id"]
admin.site.register(Post,excludeID)
admin.site.register(Comment,excludeID)
admin.site.register(Tweet,excludeID)

