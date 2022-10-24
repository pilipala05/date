# 文章管理的视图文件
from django.http import HttpResponse , JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator
import time
from datetime import datetime

from myadmin.models import Blog


# 查看用户信息
def index(request , pIndex=1):
    '''浏览信息'''
    amod = Blog.objects.get_queryset().order_by('nid')
    mywhere = []
    alist = amod.filter()

    # 获取、判断并封装关keyword键搜索
    kw = request.GET.get("keyword" , None)
    if kw:
        # 查询
        alist = alist.filter(name__contains=kw)
        mywhere.append("keyword=" + kw)

    # 执行分页处理
    pIndex = int(pIndex)
    page = Paginator(alist , 5)  # 以5条每页创建分页对象
    maxpages = page.num_pages  # 最大页数
    # 判断页数是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)  # 当前页数据
    plist = page.page_range  # 页码数列表

    # list2 = User.objects.all() #获取所有信息
    # 封装信息加载模板输出
    context = {"bloglist": list2 , 'plist': plist , 'pIndex': pIndex , 'maxpages': maxpages , 'mywhere': mywhere}
    return render(request , "myadmin/blog/index.html" , context)


    # 增加用户信息
def add(request):
    return render(request, 'myadmin/blog/add.html')


def insert(request):
    '''执行添加'''
    try:
        ob = Blog()
        ob.title = request.POST['title']
        ob.site_name = request.POST['site_name']
        ob.theme = request.POST['site_name']
        ob.save()
        context = {"info": "添加成功！"}
    except Exception as err:
        print(err)
        context = {"info": "添加失败"}
    return render(request , "myadmin/info.html" , context)

def delete(request,nid):
    '''删除信息'''
    try:
        ob = Blog.objects.get(nid=nid)
        ob.delete()
        context={"info":"删除成功！"}
    except Exception as err:
        print(err)
        context={"info":"删除失败"}
    return render(request,"myadmin/info.html",context)


def edit(request, nid):
    '''加载编辑信息页面'''
    try:
        ob = Blog.objects.get(nid=nid)
        context = {"blog": ob}
        return render(request, "myadmin/blog/edit.html", context)
    except Exception as err:
        context = {"info": "没有找到要修改的信息！"}
        return render(request, "myadmin/info.html", context)


def update(request, nid):
    '''执行编辑信息'''
    try:
        ob = Blog.objects.get(nid=nid)
        ob.title = request.POST['title']
        ob.site_name = request.POST['site_name']
        ob.theme = request.POST['theme']
        ob.save()
        context = {"info": "修改成功！"}
    except Exception as err:
        print(err)
        context = {"info": "修改失败"}
    return render(request, "myadmin/info.html", context)
