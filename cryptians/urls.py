"""cryptians URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from django.urls import include
from django.views.static import serve
from django.conf.urls import url
from django.conf import settings
from login import views as v
from django.conf.urls.static import static
from rest_framework.authtoken import  views
from mysite import views as mysiteViews
from demoAccount import views as demoAccountViews
admin.site.site_header = 'CRYPTIANS'                 
admin.site.index_title = 'Features area'
admin.site.site_title = 'Adminsitration'

urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token, name='api-token-auth'),
    path('api/login/', v.login),
    path('api/mypost/', mysiteViews.MyPostList),
    path('api/history/', demoAccountViews.historyList),
    path('', include('mysite.urls', namespace='mysite')),
    path('', include('predict.urls', namespace='predict')),
    path('', include('demoAccount.urls', namespace='demoAccount')),
    path('admin/', admin.site.urls, name='administrator'),
    path("register/", v.register, name="register"),
    path('', include("django.contrib.auth.urls")),
    path('', include('social_django.urls', namespace='social')),
    path('logout/',LogoutView.as_view(template_name=settings.LOGOUT_REDIRECT_URL),name='logout'),
    # path('', views.index, name='index'),
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = 'mysite.views.custom_page_not_found_view'
handler500 = 'mysite.views.custom_error_view'
handler403 = 'mysite.views.custom_permission_denied_view'
handler400 = 'mysite.views.custom_bad_request_view'
# http http://localhost:8000/api-token-auth/ -H 'Authorization: Token 9db0943a28454e4294cd5483e7bc8f545338b96a'