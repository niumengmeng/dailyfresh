# coding=utf-8
from django.shortcuts import render, redirect
from .models import *
from hashlib import sha1
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from . import user_decorator

from df_goods.models import GoodsInfo
from df_order.models import OrderInfo, OrderDetailInfo
from django.core.paginator import Paginator



def register(request):
    return render(request, 'df_user/register.html')


def register_handle(request):
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    upwd2 = post.get('cpwd')
    uemail = post.get('email')
    print(uemail)
    if upwd == upwd2:
        user = userInfo()
        user.uname = uname
        # 使用sha1加密
        s1 = sha1()
        s1.update(upwd)
        upwd3 = s1.hexdigest()

        user.upwd = upwd3
        user.uemail = uemail
        user.ushou = ''
        user.uaddress = ''
        user.uyoubian = ''
        user.uphone = ''
        user.save()
        return redirect('/user/login/')
    else:
        return redirect('/user/register/')


def name_exit(request, rname):
    count = userInfo.objects.filter(uname=rname).count()

    return JsonResponse({'data': count})


def login(request):
    name = request.COOKIES.get('name')
    context = {'error_name': 0, 'error_pwd': 0, 'name': name, 'pwd': ''}
    return render(request, 'df_user/login.html', context)


def login_handle(request):
    post = request.POST
    username = post.get('username')
    pwd = post.get('pwd').encode('utf-8')
    checkbox = post.get('checkbox', 0)


    user = userInfo.objects.filter(uname=username)

    if len(user) == 1:
        # 对密码加密比对数据库
        s1 = sha1()
        s1.update(pwd)
        pwd1 = s1.hexdigest()
        # 得到从哪个页面跳转到登录页面的原地址
        url = request.COOKIES.get('user', '/')
        red = HttpResponseRedirect(url)

        if pwd1 == user[0].upwd:
            if checkbox == 1:
                red.set_cookie('name', username)
            else:
                red.set_cookie('name', '', max_age=-1)

            # 系统全局使用
            request.session['user_id'] = user[0].id
            request.session['user_name'] = user[0].uname
            return red
        else:
            context = {'error_name': 0, 'error_pwd': 1, 'name': username, 'pwd': pwd}
            return render(request, 'df_user/login.html', context)

    else:
        context = {'error_name': 1, 'error_pwd': 0, 'name': username, 'pwd': pwd}
        return render(request, 'df_user/login.html', context)


def login_out(request):
    request.session.flush()
    return redirect('/')


def session_handle(request):

    if request.session.has_key('user_id'):
        user_id = request.session['user_id']
        user_name = request.session['user_name']
        state = 1
    else:
        user_id = ''
        user_name = ''
        state = 0
    print(state)
    return JsonResponse({'user_id': user_id, 'user_name': user_name, 'state': state})


@user_decorator.login
def info(request):
    uid = request.session['user_id']
    user = userInfo.objects.filter(id=uid)
    goods_id = request.COOKIES.get('goods_ids', '')
    goodslist = []
    if goods_id != '':
        goods_ids = goods_id.split(',')
        for i in goods_ids:
            print(i)
            goodslist.append(GoodsInfo.objects.get(id=int(i)))

    context = {'uname': user[0].uname, 'uphone': user[0].uphone,
               'uaddress': user[0].uaddress, 'goodslist': goodslist,
               }

    return render(request, 'df_user/user_center_info.html', context)

@user_decorator.login
def order(request):
    uid = request.session['user_id']
    orderInfo = OrderInfo.objects.filter(user_id=uid)

    detail_list = []
    for info in orderInfo:
        orderDetail = OrderDetailInfo.objects.filter(order_id=info.oid)
        for i in orderDetail:
            detail_list.append(i)

    context = {'orderInfo': orderInfo, 'detail_list': detail_list}

    return render(request, 'df_user/user_center_order.html', context)

@user_decorator.login
def site(request):
    user = userInfo.objects.filter(id=request.session['user_id'])
    context = {'address': user[0].uaddress}
    return render(request, 'df_user/user_center_site.html', context)


def site_handle(request):
    user = userInfo.objects.get(id=request.session['user_id'])

    post = request.POST
    user.ushou = post.get('site_name')
    user.uaddress = post.get('site_address')
    user.uyoubian = post.get('site_youbian')
    user.uphone = post.get('site_phone')
    user.save()
    return redirect('/user/site/')
