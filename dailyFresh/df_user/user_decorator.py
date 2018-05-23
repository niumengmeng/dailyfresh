#coding=utf-8
from django.shortcuts import redirect
from django.http import HttpResponseRedirect


#如果没有登录则转到登录界面
def login(func):

    def login_func(request, *args, **kwargs):
        if request.session.has_key('user_id'):
            return func(request,  *args, **kwargs)
        else:
            # request.get_full_path() 表示获取全部路径 包括参数等
            # request.path() 表示获取请求路径 不包括参数等
            red = HttpResponseRedirect('/user/login')
            red.set_cookie('user', request.get_full_path())
            return red
    return login_func