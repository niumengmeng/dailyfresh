#coding=utf-8
from django.shortcuts import render,redirect
from .models import *
from hashlib import sha1
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect


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
    pwd = post.get('pwd')
    checkbox = post.get('checkbox', 0)
    s1 = sha1()
    s1.update(pwd)
    pwd1 = s1.hexdigest()
    user = userInfo.objects.filter(uname=username)

    if len(user) == 1:
        red = HttpResponseRedirect('/user/info/')

        if pwd1 == user[0].upwd:
            if checkbox == 1:
                red.set_cookie('name', username)
            else:
                red.set_cookie('name', '', max_age=-1)

            request.session['user_id'] = user[0].id
            request.session['user_name'] = user[0].uname
            return red
        else:
            context = {'error_name': 0, 'error_pwd': 1, 'name': username, 'pwd': pwd}
            return render(request, 'df_user/login.html', context)

    else:
        context = {'error_name': 1, 'error_pwd': 0, 'name': username, 'pwd': pwd}
        return render(request, 'df_user/login.html', context)


def info(request):
    uid = request.session['user_id']
    user = userInfo.objects.filter(id=uid)
    context = {'uname': user[0].uname, 'uphone': user[0].uphone, 'uaddress': user[0].uaddress}
    return render(request, 'df_user/user_center_info.html', context)


def order(request):
    context = {}
    return render(request, 'df_user/user_center_order.html', context)


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
