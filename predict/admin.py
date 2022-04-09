from django.contrib import admin
from .models import btc_30M, btc_1H, btc_1D, eth_30M, eth_1H, eth_1D, ada_30M, ada_1H, ada_1D

admin.site.register(btc_30M)
admin.site.register(btc_1H)
admin.site.register(btc_1D)

admin.site.register(eth_30M)
admin.site.register(eth_1H)
admin.site.register(eth_1D)

admin.site.register(ada_30M)
admin.site.register(ada_1H)
admin.site.register(ada_1D)

