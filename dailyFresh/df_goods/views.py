#coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.core.paginator import *


def index(request):
    typelist = TypeInfo.objects.all()
    type0 = typelist[0]
    type1 = typelist[1]
    type2 = typelist[2]
    type3 = typelist[3]
    type4 = typelist[4]
    type5 = typelist[5]
    type00 = typelist[0].goodsinfo_set.order_by('id')[0:4]
    type11 = typelist[1].goodsinfo_set.order_by('id')[0:4]
    type22 = typelist[2].goodsinfo_set.order_by('id')[0:4]
    type33 = typelist[3].goodsinfo_set.order_by('id')[0:4]
    type44 = typelist[4].goodsinfo_set.order_by('id')[0:4]
    type55 = typelist[5].goodsinfo_set.order_by('id')[0:4]
    type000 = typelist[0].goodsinfo_set.order_by('-gclick')[0:4]
    type111 = typelist[1].goodsinfo_set.order_by('-gclick')[0:4]
    type222 = typelist[2].goodsinfo_set.order_by('-gclick')[0:4]
    type333 = typelist[3].goodsinfo_set.order_by('-gclick')[0:4]
    type444 = typelist[4].goodsinfo_set.order_by('-gclick')[0:4]
    type555 = typelist[5].goodsinfo_set.order_by('-gclick')[0:4]

    context = {'type0': type0, 'type00': type00, 'type1': type1, 'type11': type11, 'type2': type2,
               'type22': type22, 'type3': type3, 'type33': type33, 'type4': type4, 'type44': type44,
               'type5': type5, 'type55': type55, 'type000': type000, 'type111': type111, 'type222': type222,
               'type333': type333, 'type444': type444, 'type555': type555,
               }
    return render(request, 'df_goods/index.html', context)

# tid 类型, bid 商品id
def detail(request, tid, bid):
    # 获取用户id
    uid = request.session['user_id']
    typeinfo = TypeInfo.objects.get(pk=tid)
    typelist = TypeInfo.objects.all()
    news = typeinfo.goodsinfo_set.order_by('-id')[0:2]

    goods = GoodsInfo.objects.get(id=bid)
    goods.gclick=goods.gclick+1
    goods.save()

    type0 = typelist[0]
    type1 = typelist[1]
    type2 = typelist[2]
    type3 = typelist[3]
    type4 = typelist[4]
    type5 = typelist[5]
    context = {'news': news, 'goods': goods, 'typeinfo': typeinfo, 'uid': uid,
               'type0': type0, 'type1': type1, 'type2': type2, 'type3': type3,
               'type4': type4, 'type5': type5,
               }

    goods_ids = request.COOKIES.get('goods_ids', '')
    goods_id = str(goods.id)
    # 判断cookie是否有最近浏览
    if goods_ids != '':
        goodslist = goods_ids.split(',')
        # 如果cookie中已有这个值则移除cookie中的这个值
        if goodslist.count(goods_id)>=1:
            goodslist.remove(goods_id)
        # 插入在最前面
        goodslist.insert(0, goods_id)
        # 如果cookie中的值大于五个 则删除cookie中最后一个
        if len(goodslist)>=5:
            goodslist.pop()
        goods_ids = ','.join(goodslist)
        # 没有直接把当前商品添加上
    else:
        goods_ids = goods_id
    response = render(request, 'df_goods/detail.html', context)
    response.set_cookie('goods_ids', goods_ids)

    return response


# tid 类型 way ,排序方式 ,index 分页：当前页
def list(request, tid, way, index):
    typeinfo = TypeInfo.objects.get(pk=tid)
    typelist = TypeInfo.objects.all()
    news = typeinfo.goodsinfo_set.order_by('-id')[0:2]
    type0 = typelist[0]
    type1 = typelist[1]
    type2 = typelist[2]
    type3 = typelist[3]
    type4 = typelist[4]
    type5 = typelist[5]
    if way == '1':
        goodslist = typeinfo.goodsinfo_set.order_by('-id')
    elif way == '2':
        goodslist = typeinfo.goodsinfo_set.order_by('-gprice')
    else:
        goodslist = typeinfo.goodsinfo_set.order_by('-gclick')
    paginator = Paginator(goodslist, 10)
    page = paginator.page(int(index))

    context = {'page': page, 'paginator': paginator, "goodslist": goodslist,
               'news': news, 'way': way, 'tid': tid, 'typeinfo': typeinfo,
               'type0': type0, 'type1': type1, 'type2': type2, 'type3': type3,
               'type4': type4, 'type5': type5, }
    return render(request, 'df_goods/list.html', context)