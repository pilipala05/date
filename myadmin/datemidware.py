    #这个中间件主要作用于后台管理员登录操作
from django.urls import reverse
from django.shortcuts import redirect
import re


class DateMidware(object):
    def __init__(self, get_response):   #这个方法会在服务器启动的时候就调用  一次
        self.get_response = get_response
        # One-time configuration and initialization.
        print("DateMidware服务正常启动")
    def __call__(self, request):    #每一次的访问这个方法都会执行
        # 获取当前请求路径 便于查找出错误
        path = request.path
        print("url:",path)
        #判断是否有权限能够进入到后台
        #定义后台不登陆也可访问的列表
        urllist=['/myadmin/login','/myadmin/logout','/myadmin/dologin','/myadmin/verify']
        #判断当前所访问的页面是否能够进入、并且执行重定向
        if re.match(r'^/myadmin',path) and (path not in urllist):
            if "adminuser" not in request.session:  #判断当前管理员是否已经登录
                return redirect(reverse('myadmin_login'))   #重定向
        weburllist=['/myweb/index','myweb/index/login','myweb/index/register','myweb/index/dologin','myweb/index/insert','myweb/index/verify','myweb/index/logout']
        if re.match(r'^/home' , path) and (path not in weburllist):
            if "webuser" not in request.session:  # 判断当前管理员是否已经登录
                return redirect(reverse('myweb_index'))  # 重定向
        response=self.get_response(request)
        return response
