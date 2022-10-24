from myweb.views import index
from django.db.models import Q , F
from django.http import HttpResponse
from django.shortcuts import render , redirect
from django.urls import reverse
import time
from datetime import datetime
from myadmin.models import Article , Category , Blog , Commit , UpAndDown , Collect , Webuser , Info
from django.utils import timezone as datetime
#主页显示
def home(request):
    amod = Article.objects.get_queryset().order_by('-up_num')
    mywhere = []
    alist = amod.filter(status__lt=3)
    # 获取、判断并封装关keyword键搜索
    kw = request.GET.get("keyword" , None)
    if kw:
        # 查询
        alist = alist.filter(Q(name__contains=kw) | Q(category__title__contains=kw) | Q(blog__webuser__nickname__contains=kw))
        mywhere.append("keyword=" + kw)
    # 获取、判断并封装状态status搜索条件
    status = request.GET.get('status' , '')
    if status != '':
        alist = alist.filter(status=status)
        mywhere.append("status=" + status)
    context = {"articlelist": alist ,'mywhere': mywhere}
    return render(request , 'myweb/home/home.html' , context)
    #用户浏览文章
def article(request,aid):
    article = Article.objects.get(id=aid)
    commit_list = article.commit_set.all()
    context = {'article':article,'commit_list':commit_list}
    return render(request,'myweb/home/article.html',context)

    #用户发布文章
def addarticle(request):
    ctype = Category.objects.all()
    btype = Blog.objects.all()
    context = {"ctype": ctype , "btype": btype}
    return render(request , 'myweb/home/addarticle.html' , context)

    #执行发布文章
def insertarticle(request):
    '''执行添加'''
    try:
        blog_id = request.session.session_key
        # 上传图片操作
        # 图片的上传处理
        myfile = request.FILES.get("picture" , None)
        if not myfile:
            return HttpResponse("没有封面上传文件信息")
        picture = str(time.time()) + "." + myfile.name.split('.').pop()
        destination = open("./static/uploads/article/" + picture , "wb+")
        for chunk in myfile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
        message = request.POST.get('message')
        from bs4 import BeautifulSoup   #处理xss攻击
        soup = BeautifulSoup(message,'html.parser') #过滤掉了html
        tags = soup.find_all()
        for tag in tags:
            if tag.name == 'script':
                tag.decompose()
        # 封装
        ob = Article()
        ob.message = str(soup)
        ob.picture = picture
        ob.name = request.POST['name']
        ob.main = request.POST['main']
        ob.blog_id = request.POST['blog']
        ob.category_id = request.POST['category']
        ob.status = 1
        ob.publish_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        return redirect(reverse('myweb_home'))
    except Exception as err:
        print(err)
        context = {"info": "添加失败"}
    return render(request , "myadmin/info.html" , context)

    #发布评论
def commit(request):
    try:
        ob = Commit()
        ob.article_id = request.POST.get('article_id')
        ob.webuser_id = request.POST.get('webuser_id')
        ob.content = request.POST.get('content')
        ob.parent_id = request.POST.get('parent_id')
        ob.save()
        context = {'info':'发布成功'}
    except Exception as err:
        print(err)
        context = {"info": "发布失败"}
    return render(request, "myadmin/info.html" , context)

#删除文章
def article_del(request):
    nid = request.POST.get('article_id')
    try:
        ob = Article.objects.get(id=nid)
        ob.delete()
        context = {"info": "删除成功！"}
    except Exception as err:
        print(err)
        context = {"info": "删除失败"}
    return render(request , "myadmin/info.html" , context)

#删除评论
def del_commit(request):
    nid = request.POST.get('del_id')
    try:
        ob = Commit.objects.get(nid=nid)
        ob.delete()
        context = {"info": "删除成功！"}
    except Exception as err:
        print(err)
        context = {"info": "删除失败"}
    return render(request , "myadmin/info.html" , context)

    #点赞
def aup(request):
    webuser_id = request.POST.get('webuser_id')
    article_id = request.POST.get('article_id')
    up = UpAndDown.objects.filter(webuser_id=webuser_id,article_id=article_id).first()
    if up:
        context = {"info": "已经点过了"}
    else:
        ob = UpAndDown()
        ob.article_id = article_id
        ob.webuser_id = webuser_id
        ob.up_down = request.POST.get('up_num')
        ob.save()
        Article.objects.filter(id=article_id).update(up_num=F('up_num')+1)
        context = {"info": "点赞成功"}
    return render(request , "myadmin/info.html" , context)

#收藏功能
def collect(request):
    webuser_id = request.POST.get('webuser_id')
    article_id = request.POST.get('article_id')
    col = Collect.objects.filter(webuser_id=webuser_id,article_id=article_id).first()
    if col:
        context = {"info": "已经点过了"}
    else:
        ob = Collect()
        ob.article_id = article_id
        ob.webuser_id = webuser_id
        ob.up_down = request.POST.get('up_num')
        ob.save()
        Article.objects.filter(id=article_id).update(down_num=F('down_num')+1)
        context = {"info": "收藏成功"}
    return render(request , "myadmin/info.html" , context)

#取消收藏
def c_del(request):
    nid = request.POST.get('collect_nid')
    article_id = request.POST.get('article_id')
    try:
        ob = Collect.objects.get(nid=nid)
        ob.delete()
        Article.objects.filter(id=article_id).update(down_num=F('down_num') - 1)
        context = {"info": "取消成功！"}
    except Exception as err:
        print(err)
        context = {"info": "取消失败"}
    return render(request , "myadmin/info.html" , context)

#个人页面展示
def persional(request,wid):
    webuser = Webuser.objects.filter(id=wid).first()
    info = Info.objects.filter(webuser_id=wid).first()
    if not webuser:
        return render(request,'error.html')
    blog = webuser.blog
    #获得该论坛下的所有文章
    article_list = blog.article_set.all().order_by('publish_at')
    context = {"alist":article_list,"blog":blog,"info":info}
    return render(request,"myweb/home/persional.html",context)

#展示收藏文章
def collection(request,wid):
    webuser = Webuser.objects.filter(id=wid).first()
    info = Info.objects.filter(webuser_id=wid).first()
    collect = Collect.objects.filter(webuser_id=wid)
    if not collect:
        context = {"啥也没有"}
    blog = webuser.blog
    #获得该论坛收藏的所有文章
    article_list = Article.objects.all().order_by('-up_num')
    context = {"alist":article_list,"collect":collect,"blog":blog,"info":info}
    return render(request,"myweb/home/collection.html",context)

#分类页面展示
def cat(request,wid):
    cat = Category.objects.filter(nid=wid).first()
    if not cat:
        context = {"啥也没有"}
    # 获得该论坛收藏的所有文章
    if not cat.article_set.all():
        context={"啥也没有"}
    #取数据判断其状态、排序
    article_list = cat.article_set.filter(status__lt=2).all().order_by('-up_num')
    context = {"alist": article_list,"cat":cat.title}
    return render(request,'myweb/home/cat.html',context)

#编辑个人信息页面
def edit(request):
    return render(request,'myweb/home/edit.html')

#执行编辑信息
def update(request,wid):
    '''执行编辑信息'''
    myfile = request.FILES.get("head" , None)
    if not myfile:
        return HttpResponse("没有封面上传文件信息")
    head = str(time.time()) + "." + myfile.name.split('.').pop()
    destination = open("./static/uploads/webuser/" + head , "wb+")
    for chunk in myfile.chunks():  # 分块写入文件
        destination.write(chunk)
    destination.close()
    try:
        ob = Webuser.objects.get(id=wid)
        ob.nickname = request.POST['nickname']
        ob.mobile = request.POST['mobile']
        ob.password = request.POST['password']
        ob.head = head
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        bid = ob.blog.nid
        ob.save()
        obj = Blog.objects.get(nid=bid)
        obj.title = request.POST['blog']
        context = {"log": "修改成功！"}
        return redirect(reverse('myweb_home_edit'),context)
    except Exception as err:
        print(err)
        context = {"log": "修改失败"}
    return render(request , "myweb/log.html" , context)
#编辑简介页面
def editinfo(request):
    return render(request,"myweb/home/editinfo.html")

#执行编辑简介
def updateinfo(request,wid):
    #判断表是否存在
    try:
        ob = Info.objects.get(webuser_id=wid)
        ob.info = request.POST['info']
        ob.habit = request.POST['habit']
        ob.star = request.POST['star']
        ob.birth = request.POST['birth']
        ob.school = request.POST['school']
        ob.location = request.POST['location']
        ob.save()
        context = {"info": "修改成功"}
        return redirect(reverse('myweb_home_editinfo'))
    except Exception as err:
        print(err)
        context = {"info": "修改失败"}
    return render(request , "myadmin/info.html" , context)
