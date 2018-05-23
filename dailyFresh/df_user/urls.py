from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^register_handle/$', views.register_handle, name='register_handle'),
    url(r'^name_exit/(.+)/$', views.name_exit, name='name_exit'),
    url(r'^login/$', views.login, name='login'),
    url(r'^login_handle/$', views.login_handle, name='login_handle'),
    url(r'^login_out/$', views.login_out , name='login_out'),
    url(r'^info/$', views.info, name='info'),
    url(r'^order/$', views.order, name='order'),
    url(r'^site/$', views.site, name='site'),
    url(r'^site_handle/$', views.site_handle, name='site_handle'),
    url(r'^session_handle/$', views.session_handle, name='session_handle'),


]