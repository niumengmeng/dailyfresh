from django.shortcuts import render,redirect
from df_goods.models import GoodsInfo
from df_user.models import userInfo
from df_cart.models import CartInfo
from .models import OrderInfo,OrderDetailInfo
from df_user import user_decorator
from django.db import transaction
from datetime import datetime
from decimal import Decimal

@user_decorator.login
def order(request):
    uid = request.session['user_id']

    carts = CartInfo.objects.filter(user_id=uid)
    user = userInfo.objects.get(id=uid)

    context = {"carts": carts, 'user': user}
    return render(request, 'df_order/place_order.html', context)


# 设置事物
@transaction.atomic()
@user_decorator.login
def order_handle(request):
    # 设置事物原点
    tran_id = transaction.savepoint()
    uid = request.session['user_id']
    carts = CartInfo.objects.filter(user_id=uid)
    try:
        # 订单信息保存数据
        orderinfo = OrderInfo()
        now = datetime.now()
        orderinfo.oid = '%s%d'%(now.strftime('%Y%m%d%H%M%S'), uid)
        orderinfo.user_id = uid
        orderinfo.ototal = Decimal(request.POST.get('total'))
        orderinfo.odate = now
        orderinfo.save()
        for cart in carts:
            orderDetail = OrderDetailInfo()
            orderDetail.order = orderinfo
            goods_id = cart.goods_id
            goods = GoodsInfo.objects.get(id=goods_id)
            # 如果库存大于购买的数量，库存=库存-数量
            if goods.gkucun>cart.count:
                goods.gkucun = goods.gkucun-cart.count
                goods.save()
                # 订单详情页保存数据
                orderDetail.goods_id = goods.id
                orderDetail.count = cart.count
                orderDetail.price = goods.gprice
                orderDetail.save()
                # 删除购物车数据
                cart.delete()
            else:
                transaction.savepoint_rollback(tran_id)
                return redirect('/cart/')

        transaction.savepoint_commit(tran_id)
    except Exception as e:
        transaction.savepoint_rollback(tran_id)
    context = {'orderinfo': orderinfo, 'orderDetail':orderDetail}
    return render(request, 'df_user/user_center_order.html', context)
