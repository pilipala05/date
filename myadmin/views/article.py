# 文章管理的视图文件
from django.http import HttpResponse , JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator
import time
from datetime import datetime

from myadmin.models import Article,Category,Blog


# 查看用户信息
def index(request , pIndex=1):
    '''浏览信息'''
    amod = Article.objects.get_queryset().order_by('id')
    mywhere = []
    alist = amod.filter(status__lt=3)

    # 获取、判断并封装关keyword键搜索
    kw = request.GET.get("keyword" , None)
    if kw:
        # 查询
        alist = alist.filter(name__contains=kw)
        mywhere.append("keyword=" + kw)

    # 获取、判断并封装状态status搜索条件
    status = request.GET.get('status' ,'')
    if status != '':
        alist = alist.filter(status=status)
        mywhere.append("status=" + status)

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
    context = {"articlelist": list2 , 'plist': plist , 'pIndex': pIndex , 'maxpages': maxpages , 'mywhere': mywhere}
    return render(request , "myadmin/article/index.html" , context)


    # 增加用户信息
def add(request):
    ctype = Category.objects.all()
    btype = Blog.objects.all()
    context = {"ctype":ctype,"btype":btype}
    return render(request, 'myadmin/article/add.html',context)


def insert(request):
    '''执行添加'''
    try:
        #上传图片操作
        # 图片的上传处理
        myfile = request.FILES.get("picture", None)
        if not myfile:
            return HttpResponse("没有封面上传文件信息")
        picture = str(time.time()) + "." + myfile.name.split('.').pop()
        destination = open("./static/uploads/article/" + picture, "wb+")
        for chunk in myfile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
        #封装
        ob = Article()
        ob.message = request.POST['message']
        ob.picture = picture
        ob.name = request.POST['name']
        ob.main = request.POST['main']
        ob.blog_id = request.POST['blog']
        ob.category_id = request.POST['category']
        ob.status = 1
        ob.publish_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {"info": "添加成功！"}
    except Exception as err:
        print(err)
        context = {"info": "添加失败"}
    return render(request, "myadmin/info.html", context)

def delete(request,nid):
    '''删除信息'''
    try:
        ob = Article.objects.get(id=nid)
        ob.delete()
        context={"info":"删除成功！"}
    except Exception as err:
        print(err)
        context={"info":"删除失败"}

    return render(request,"myadmin/info.html",context)


def edit(request, nid):
    ctype = Category.objects.all()
    btype = Blog.objects.all()
    '''加载编辑信息页面'''
    try:
        ob = Article.objects.get(id=nid)
        context = {"article": ob,"ctype":ctype,"btype":btype}
        return render(request, "myadmin/article/edit.html", context)
    except Exception as err:
        context = {"info": "没有找到要修改的信息！"}
        return render(request, "myadmin/info.html", context)


def update(request, nid):
    '''执行编辑信息'''
    try:
        ob = Article.objects.get(id=nid)
        ob.status = request.POST['status']
        ob.blog_id = request.POST['blog']
        ob.category_id = request.POST['category']
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {"info": "修改成功！"}
    except Exception as err:
        print(err)
        context = {"info": "修改失败"}
    return render(request, "myadmin/info.html", context)
