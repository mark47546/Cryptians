from django.contrib import admin
from .models import User

class excludeID(admin.ModelAdmin):
    exclude = ["id"]
admin.site.register(User)