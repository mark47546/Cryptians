from django.contrib import admin
from .models import *

class excludeID(admin.ModelAdmin):
    exclude = ["id"]

admin.site.register(btc_30M,excludeID)
admin.site.register(btc_1H, excludeID)
admin.site.register(btc_1D, excludeID)

admin.site.register(eth_30M, excludeID)
admin.site.register(eth_1H), excludeID
admin.site.register(eth_1D, excludeID)

admin.site.register(bnb_30M, excludeID)
admin.site.register(bnb_1H, excludeID)
admin.site.register(bnb_1D, excludeID)

admin.site.register(ada_30M, excludeID)
admin.site.register(ada_1H, excludeID)
admin.site.register(ada_1D, excludeID)

admin.site.register(ltc_30M, excludeID)
admin.site.register(ltc_1H, excludeID)
admin.site.register(ltc_1D, excludeID)

