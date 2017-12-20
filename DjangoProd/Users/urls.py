from django.conf.urls import url
from django.contrib.auth.views import login

from . import views

urlpatterns=[
            #  登录页面
url(r'^login/$', login, {'template_name': 'users/login.html'},name='login'), 
url(r'^logout/$', views.logout_view, name='logout'),
url(r'^register/$', views.register, name='register'),
            
             ]
