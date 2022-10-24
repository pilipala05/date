import time
from datetime import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
from django.urls import reverse

from myadmin.models import Webuser , Blog , Info


def index(request):
    return render(request, 'myweb/index/index.html')

def login(request):
    return render(request , 'myweb/index/login.html')
#注册页面
def register(request):
    return render(request,'myweb/index/register.html')
#执行注册
def insert(request):
    '''执行添加'''
    try:
        # 图片的上传处理
        myfile = request.FILES.get("picture", None)
        if not myfile:
            return HttpResponse("没有头像上传文件信息")
        picture = str(time.time()) + "." + myfile.name.split('.').pop()
        destination = open("./static/uploads/webuser/" + picture, "wb+")
        for chunk in myfile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
        #创建论坛
        obj = Blog()
        obj.title = request.POST['nickname']
        obj.theme = ''
        obj.site_name = ''
        obj.save()
        #增加用户
        ob = Webuser()
        ob.nickname = request.POST['nickname']
        ob.head = picture
        ob.mobile = request.POST['mobile']
        ob.email = request.POST['email']
        ob.password = request.POST['pass']
        ob.status = 1
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.blog = obj
        ob.save()
        #增加info
        obk = Info()
        obk.info = '暂无'
        obk.star = '暂无'
        obk.habit = '暂无'
        obk.location = '暂无'
        obk.school = '暂无'
        obk.birth = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        obk.webuser = ob
        obk.save()
        context = {"info": "注册成功！"}
    except Exception as err:
        print(err)
        context = {"info": "注册失败"}
    return render(request, "myweb/index/login.html", context)
#执行登录
def dologin(request):
    try:
        # 验证判断
        verifycode = request.session['verifycode']
        code = request.POST['code']  # 获取从前端获取的code值
        if verifycode != code:
            context = {'info': '验证码错误！'}
            return render(request , "myweb/index/login.html" , context)
        # 根据登录账号获取用户信息
        webuser = Webuser.objects.get(email=request.POST['email1'])
        # 校验当前用户状态是否可用
        if webuser.status == 1:
            n = webuser.password
            s = request.POST['pass']
            # 校验密码是否正确
            if n == s:
                # 将当前登录成功用户信息以adminuser这个key放入到session中
                request.session['webuser'] = webuser.toDict()
                return redirect(reverse('myweb_home'))
            else:
                context = {"info": "登录密码错误！"}
        else:
            context = {"info": "此用户非可用账号"}
    except Exception as err:
        print(err)
        context = {"info": "登录账号不存在！"}
    return render(request , "myweb/index/login.html", context)

#退出
def logout(request):
    del request.session['webuser']
    return redirect(reverse('myweb_index'))
#验证码
def verify(request):
    # 引入随机函数模块
    import random
    from PIL import Image , ImageDraw , ImageFont
    # 定义变量，用于画面的背景色、宽、高
    bgcolor = (242 , 164 , 247)
    width = 100
    height = 25
    # 创建画面对象
    im = Image.new('RGB' , (width , height) , bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制
    for i in range(0 , 100):
        xy = (random.randrange(0 , width) , random.randrange(0 , height))
        fill = (random.randrange(0 , 255) , 255 , random.randrange(0 , 255))
        draw.point(xy , fill=fill)
    # 定义验证码的取值
    str1 = '0123456789'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0 , 4):
        rand_str += str1[random.randrange(0 , len(str1))]
    # 字体属性
    font = ImageFont.truetype('static/AGENCYB.TTF' , 21)
    # 设置字体颜色
    fontcolor = (255 , random.randrange(0 , 255) , random.randrange(0 , 255))
    # 绘制4个字
    draw.text((5 , -3) , rand_str[0] , font=font , fill=fontcolor)
    draw.text((25 , -3) , rand_str[1] , font=font , fill=fontcolor)
    draw.text((50 , -3) , rand_str[2] , font=font , fill=fontcolor)
    draw.text((75 , -3) , rand_str[3] , font=font , fill=fontcolor)
    # 释放画笔
    del draw
    # 存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    # 内存文件操作
    import io
    buf = io.BytesIO()
    # 将图片保存在内存中
    im.save(buf , 'png')
    # 将内存中的图片数据返回给客户端
    return HttpResponse(buf.getvalue() , 'image/png')


