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

admin.site.site_header = 'CRYPTIANS'                 
admin.site.index_title = 'Features area'
admin.site.site_title = 'Adminsitration'

urlpatterns = [
    path('', include('mysite.urls', namespace='mysite')),
    path('tinymce/', include('tinymce.urls')),
    path('admin/', admin.site.urls, name='administrator'),
    path("register/", v.register, name="register"),
    path('', include("django.contrib.auth.urls")),
    path('', include('social_django.urls', namespace='social')),
    path('logout/',LogoutView.as_view(template_name=settings.LOGOUT_REDIRECT_URL),name='logout'),
    # path('', views.index, name='index'),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]
