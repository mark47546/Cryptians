from django.urls import path
from predict import views
# from .views import DrawingDetail
app_name = 'predict'

urlpatterns = [
    path('predict/', views.predict, name='predict'),
    path('predict/btc/lstm/30m', views.lstm_btc_30M, name='lstm_btc_30M'),
    path('predict/btc/lstm/1h', views.lstm_btc_1H, name='lstm_btc_1H'),
    path('predict/btc/lstm/1d', views.lstm_btc_1D, name='lstm_btc_1D'),
    path('predict/btc/lrg/30m', views.lrg_btc_30M, name='lrg_btc_30M'),
    path('predict/btc/lrg/1h', views.lrg_btc_1H, name='lrg_btc_1H'),
    path('predict/btc/lrg/1d', views.lrg_btc_1D, name='lrg_btc_1D'),

    path('predict/ada/lstm/30m', views.lstm_ada_30M, name='lstm_ada_30M'),
    path('predict/ada/lstm/1h', views.lstm_ada_1H, name='lstm_ada_1H'),
    path('predict/ada/lstm/1d', views.lstm_ada_1D, name='lstm_ada_1D'),
    path('predict/ada/lrg/30m', views.lrg_ada_30M, name='lrg_ada_30M'),
    path('predict/ada/lrg/1h', views.lrg_ada_1H, name='lrg_ada_1H'),
    path('predict/ada/lrg/1d', views.lrg_ada_1D, name='lrg_ada_1D'),

    path('predict/eth/lstm/30m', views.lstm_eth_30M, name='lstm_eth_30M'),
    path('predict/eth/lstm/1h', views.lstm_eth_1H, name='lstm_eth_1H'),
    path('predict/eth/lstm/1d', views.lstm_eth_1D, name='lstm_eth_1D'),
    path('predict/eth/lrg/30m', views.lrg_eth_30M, name='lrg_eth_30M'),
    path('predict/eth/lrg/1h', views.lrg_eth_1H, name='lrg_eth_1H'),
    path('predict/eth/lrg/1d', views.lrg_eth_1D, name='lrg_eth_1D'),

    path('predict/bnb/lstm/30m', views.lstm_bnb_30M, name='lstm_bnb_30M'),
    path('predict/bnb/lstm/1h', views.lstm_bnb_1H, name='lstm_bnb_1H'),
    path('predict/bnb/lstm/1d', views.lstm_bnb_1D, name='lstm_bnb_1D'),
    path('predict/bnb/lrg/30m', views.lrg_bnb_30M, name='lrg_bnb_30M'),
    path('predict/bnb/lrg/1h', views.lrg_bnb_1H, name='lrg_bnb_1H'),
    path('predict/bnb/lrg/1d', views.lrg_bnb_1D, name='lrg_bnb_1D'),

    path('predict/ltc/lstm/30m', views.lstm_ltc_30M, name='lstm_ltc_30M'),
    path('predict/ltc/lstm/1h', views.lstm_ltc_1H, name='lstm_ltc_1H'),
    path('predict/ltc/lstm/1d', views.lstm_ltc_1D, name='lstm_ltc_1D'),
    path('predict/ltc/lrg/30m', views.lrg_ltc_30M, name='lrg_ltc_30M'),
    path('predict/ltc/lrg/1h', views.lrg_ltc_1H, name='lrg_ltc_1H'),
    path('predict/ltc/lrg/1d', views.lrg_ltc_1D, name='lrg_ltc_1D'),

]