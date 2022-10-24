"""date URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# 前端子路由配置
from django.urls import path

from myweb.views import index
from myweb.views import home
urlpatterns = [
    path('', index.index, name="myweb_index"),
    path('index/login' , index.login , name="myweb_index_login") ,
    path('index/register',index.register,name="myweb_index_register"),#注册
    path('index/insert',index.insert,name="myweb_index_insert"),#执行注册
    path('index/dologin' , index.dologin , name="myweb_index_dologin") ,
    path('index/logout' , index.logout , name="myweb_index_logout") ,
    path('index/verify' , index.verify , name="myweb_index_verify") ,  # 验证码
    #主页面
    path('home',home.home,name='myweb_home'),
    #文章展示页面
    path('home/article/<int:aid>',home.article,name="myweb_home_article"),
    #发布文章页面
    path('home/addarticle',home.addarticle,name="myweb_home_addarticle"),
    #文章删除
    path('article_del',home.article_del,name="article_del"),
    #点赞
    path('aup',home.aup,name="aup"),
    #收藏
    path('collect',home.collect,name="collect"),
    #取消收藏
    path('c_del',home.c_del,name="c_del"),
    #收藏展示页面
    path('home/collection/<int:wid>',home.collection,name="myweb_home_collection"),
    #发表评论
    path('commit',home.commit,name="commit"),
    #删除评论
    path('del_commit',home.del_commit,name="del_commit"),
    #执行添加文章
    path('home/insertarticle',home.insertarticle,name="myweb_home_insertarticle"),
    #个人页面展示
    path('home/persional/<int:wid>',home.persional,name="myweb_home_persional"),
    #分类主页面
    path('home/cat/<int:wid>',home.cat,name="myweb_home_cat"),
    #个人信息页面
    path('home/edit',home.edit,name="myweb_home_edit"),
    #执行编辑
    path('home/update/<int:wid>',home.update,name="myweb_home_update"),
    # 个人简介
    path('home/editinfo' , home.editinfo , name="myweb_home_editinfo") ,
    # 执行编辑简介内容
    path('home/updateinfo/<int:wid>' , home.updateinfo , name="myweb_home_updateinfo") ,

]
