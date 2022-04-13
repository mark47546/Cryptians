from django.urls import path
from demoAccount import views
# from .views import DrawingDetail
app_name = 'demoAccount'

urlpatterns = [
    path('demoaccount/', views.DemoAccount, name='DemoAccount'),
    path('demoaccount/trade/btc/', views.tradeBTC, name='tradeBTC'),
    path('demoaccount/trade/eth/', views.tradeETH, name='tradeETH'),
    path('demoaccount/trade/bnb/', views.tradeBNB, name='tradeBNB'),
    path('demoaccount/trade/ada/', views.tradeADA, name='tradeADA'),
    path('demoaccount/trade/ltc/', views.tradeLTC, name='tradeLTC'),
    path('demoaccount/history/',views.history, name='history')
]