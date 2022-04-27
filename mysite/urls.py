from django.urls import path
from mysite import views
# from .views import DrawingDetail
app_name = 'mysite'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('allPost/',views.allPost, name='allPost'),
    path('tag/<slug:slug>/', views.tagged, name="tagged"),
    path('allPost/<str:post_id>',views.viewPost, name='viewPost'),
    path('createPost/',views.createPost, name='createPost'),

    path('myPost/',views.myPost, name='myPost'),
    path('myPost/edit/<str:post_id>',views.editPost, name='editPost'),
    path('myPost/update/<str:post_id>',views.updatePost, name='updatePost'),
    path('myPost/delete/<str:post_id>',views.deletePost, name='deletePost'),
    path('allPost/<str:post_id>/deleteComment/<str:comment_id>/',views.deleteComment, name='deleteComment'),

    path('tweet_list/',views.tweet_list, name='tweet_list'),
    path('realtime_graph/',views.realtime_graph, name='realtime_graph'),

]