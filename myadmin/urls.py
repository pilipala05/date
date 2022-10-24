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

# 后台管理的子路由
from django.urls import path
from myadmin.views import index , webuser , blog , category
from myadmin.views import user
from myadmin.views import article
# 后台管理子路由
urlpatterns = [
    path('' , index.index , name="myadmin_index") ,  # 后台页面
    #浏览web用户路由
    path('webuser/<int:pIndex>', webuser.index, name="myadmin_webuser_index"),
    path('webuser/delete<int:uid>', webuser.delete, name="myadmin_webuser_delete"),
    path('webuser/edit<int:uid>', webuser.edit, name="myadmin_webuser_edit"),
    path('webuser/update/<int:uid>', webuser.update, name="myadmin_webuser_update"),

    #后台管理员登录退出路由
    path('login',index.login,name="myadmin_login"),
    path('dologin',index.dologin,name="myadmin_dologin"),
    path('logout',index.logout,name="myadmin_logout"),
    path('verify',index.verify,name="myadmin_verify"),   #验证码

    #文章信息管理路由配置
    path('article/<int:pIndex>' , article.index , name="myadmin_article_index"),
    path('article/add' , article.add , name="myadmin_article_add"),
    path('article/insert' , article.insert , name="myadmin_article_insert"),
    path('article/delete/<int:nid>', article.delete , name="myadmin_article_delete"),
    path('article/edit/<int:nid>', article.edit, name="myadmin_article_edit") ,  # 准备信息编辑
    path('article/update/<int:nid>', article.update, name="myadmin_article_update") ,  # 执行信息编辑

    #博客信息管理路由
    path('blog/<int:pIndex>' , blog.index , name="myadmin_blog_index"),
    path('blog/add' , blog.add , name="myadmin_blog_add"),
    path('blog/insert' , blog.insert , name="myadmin_blog_insert"),
    path('blog/delete/<int:nid>', blog.delete , name="myadmin_blog_delete"),
    path('blog/edit/<int:nid>', blog.edit, name="myadmin_blog_edit") ,  # 准备信息编辑
    path('blog/update/<int:nid>', blog.update, name="myadmin_blog_update") ,

    #分类管理路由
    path('category/<int:pIndex>' , category.index , name="myadmin_category_index"),
    path('category/add' , category.add , name="myadmin_category_add"),
    path('category/insert' , category.insert , name="myadmin_category_insert"),
    path('category/delete/<int:nid>', category.delete , name="myadmin_category_delete"),
    path('category/edit/<int:nid>', category.edit, name="myadmin_category_edit") ,  # 准备信息编辑
    path('category/update/<int:nid>', category.update, name="myadmin_category_update") ,

    # 用户信息管理路由设置
    path('user/<int:pIndex>' , user.index , name="myadmin_user_index"),
    path('user/add' , user.add , name="myadmin_user_add"),
    path('user/insert' , user.insert , name="myadmin_user_insert"),
    path('user/delete/<int:uid>', user.delete , name="myadmin_user_delete"),
    path('user/edit/<int:uid>', user.edit, name="myadmin_user_edit") ,  # 准备信息编辑
    path('user/update/<int:uid>', user.update, name="myadmin_user_update") ,  # 执行信息编辑
    #博客管理路由设置



]
