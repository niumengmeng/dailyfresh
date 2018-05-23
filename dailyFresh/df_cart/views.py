# coding=utf-8
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import CartInfo
from df_goods.models import *
from df_user import user_decorator


@user_decorator.login
def cart(request):
    uid = request.session['user_id']
    carts = CartInfo.objects.filter(user_id=uid)

    context = {'carts': carts}
    return render(request, 'df_cart/cart.html', context)


@user_decorator.login
def add(request, goodsid, count):
    uid = request.session['user_id']
    count = int(count)
    carts = CartInfo.objects.filter(user_id=uid, goods_id=goodsid)
    if len(carts) > 0:
        carts[0].count += count
        carts[0].save()
    else:
        cart = CartInfo()
        cart.user_id = uid
        cart.goods_id = goodsid
        cart.count = count
        cart.save()
    context = {}
    if request.is_ajax():
        count = CartInfo.objects.filter(user_id=uid).count()
        return JsonResponse({'count': count})
    else:
        return render(request, 'df_cart/cart.html', context)


# 返回购物车数量默认值
def cart_num(request):
    uid = request.session['user_id']
    count = CartInfo.objects.filter(user_id=uid).count()
    return JsonResponse({'count': count})


def edit_cart(request, cart_id, count):
    cart = CartInfo.objects.get(id=cart_id)
    cart.count = int(count)
    cart.save()
    return JsonResponse({'ok': 1})


# 删除
def delete(request, cart_id):
    try:
        cart = CartInfo.objects.get(id=cart_id)
        cart.delete()
        data = {'ok': 1}
    except Exception as e:
        data = {'ok': e}

    return JsonResponse(data)