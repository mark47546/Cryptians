from django.contrib import admin
from .models import demoAccount, Trade

class excludeID(admin.ModelAdmin):
    exclude = ["id"]
admin.site.register(demoAccount, excludeID)
admin.site.register(Trade, excludeID)
