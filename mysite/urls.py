from django.urls import path
from mysite import views
# from .views import DrawingDetail
app_name = 'mysite'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('allpost/',views.allPost, name='allpost'),
]