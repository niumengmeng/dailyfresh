from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.cart, name='cart'),
    url(r'^add_(\d+)_(\d+)/$', views.add, name='add'),
    url(r'^cart_num', views.cart_num, name='cart_num'),
    url(r'^eidt_(\d+)_(\d+)/', views.edit_cart, name='edit_cart'),
    url(r'^delete_(\d+)/', views.delete, name='delete'),
]