from django.urls import path
from mysite import views
# from .views import DrawingDetail
app_name = 'mysite'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('allPost/',views.allPost, name='allPost'),
    path('allPost/<str:post_id>',views.viewPost, name='viewPost'),
    path('createPost/',views.createPost, name='createPost'),
]