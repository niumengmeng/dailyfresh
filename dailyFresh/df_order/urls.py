from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.order, name='order'),
    url(r'^order_handle/$', views.order_handle, name='order_handle'),
]