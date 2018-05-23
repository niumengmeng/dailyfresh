# coding=utf-8
from django.shortcuts import render, redirect
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

# 添加商品到购物车
@user_decorator.login
def add(request, goodsid, count):
    uid = request.session['user_id']
    count = int(count)
    carts = CartInfo.objects.filter(user_id=uid, goods_id=goodsid)
    # 判断购物车是否已经有这个商品，有：数量+1 没有：把商品存入
    if len(carts) > 0:
        carts[0].count += count
        carts[0].save()
    else:
        cart = CartInfo()
        cart.user_id = uid
        cart.goods_id = goodsid
        cart.count = count
        cart.save()
   
    if request.is_ajax():
        count = CartInfo.objects.filter(user_id=uid).count()
        return JsonResponse({'count': count})
    else:
        return redirect('/cart/')


# 返回购物车数量默认值
def cart_num(request):
    uid = request.session['user_id']
    count = CartInfo.objects.filter(user_id=uid).count()
    return JsonResponse({'count': count})

# 修改商品数量
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