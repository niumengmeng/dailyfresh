from django.conf.urls import url
from . import views
from .views import MysearchView
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index/$', views.index, name='index'),
    url(r'^detail_(\d+)_(\d+)/$', views.detail, name='detail'),
    url(r'^list_(\d+)_(\d+)_(\d+)/$', views.list, name='list'),
    url(r'^search/', MysearchView()),

]