#coding=utf-8
from django.shortcuts import render,redirect
from .models import *
from hashlib import sha1


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
        upwd3 = s1.hexdigest().decode('utf-8')

        user.upwd = upwd
        user.uemail = uemail
        user.ushou = ''
        user.uaddress = ''
        user.uyoubian = ''
        user.uphone = ''
        user.save()
        return redirect('/user/login/')
    else:
        return redirect('/user/register/')


def login(request):

    return render(request, 'df_user/login.html')