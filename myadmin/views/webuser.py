#前端用户信息管理视图
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from datetime import datetime
from myadmin.models import Webuser , Blog


#浏览
def index(request , pIndex=1):
    '''浏览信息'''
    umod = Webuser.objects.get_queryset().order_by('id')
    mywhere = []
    list = umod.filter(status__lt=3)
    # 获取、判断并封装关keyword键搜索
    kw = request.GET.get("keyword" , None)
    if kw:
        # 查询员工账号或昵称中只要含有关键字的都可以
        list = list.filter(Q(nickname__contains=kw) | Q(email__contains=kw))
        mywhere.append("keyword=" + kw)

    # 获取、判断并封装状态status搜索条件
    status = request.GET.get('status' , '')
    if status != '':
        list = list.filter(status=status)
        mywhere.append("status=" + status)

    # 执行分页处理
    pIndex = int(pIndex)
    page = Paginator(list , 5)  # 以5条每页创建分页对象
    maxpages = page.num_pages  # 最大页数
    # 判断页数是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)  # 当前页数据
    plist = page.page_range  # 页码数列表
    context = {"webuserlist": list2 , 'plist': plist , 'pIndex': pIndex , 'maxpages': maxpages , 'mywhere': mywhere}
    return render(request , "myadmin/webuser/index.html" , context)
#删除
def delete(request,uid):
    '''删除信息'''
    try:
        ob = Webuser.objects.get(id=uid)
        ob.delete()
        context={"info":"删除成功！"}
    except Exception as err:
        print(err)
        context={"info":"删除失败"}
    return render(request,"myadmin/info.html",context)


def edit(request, uid):
    btype = Blog.objects.all()
    '''加载编辑信息页面'''
    try:
        ob = Webuser.objects.get(id=uid)
        context = {"webuser": ob,"btype":btype}
        return render(request, "myadmin/webuser/edit.html", context)
    except Exception as err:
        context = {"info": "没有找到要修改的信息！"}
        return render(request, "myadmin/info.html", context)

def update(request, uid):
    '''执行编辑信息'''
    try:
        ob = Webuser.objects.get(id=uid)
        ob.status = request.POST['status']
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.blog_id = request.POST['blog']
        ob.save()
        context = {"info": "修改成功！"}
    except Exception as err:
        print(err)
        context = {"info": "修改失败"}
    return render(request, "myadmin/info.html", context)