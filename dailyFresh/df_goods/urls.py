from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index/$', views.index, name='index'),
    url(r'^detail_(\d+)_(\d+)/$', views.detail, name='index'),
    url(r'^list_(\d+)_(\d+)_(\d+)/$', views.list, name='index'),


]