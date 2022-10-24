from datetime import datetime

from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.
  #用户账号信息模型

class User(models.Model):
    username = models.CharField(max_length=50)    #用户账号
    nickname = models.CharField(max_length=50)    #昵称
    password_hash = models.CharField(max_length=100)  #密码
    password_salt = models.CharField(max_length=50)    #密码干扰值
    status = models.IntegerField(default=1)    #状态:1正常/6.管理员/2禁用/9删除
    create_at = models.DateTimeField(default=datetime.now)    #创建时间
    update_at = models.DateTimeField(default=datetime.now)    #修改时间

    def toDict(self):
        return {'id':self.id,'username':self.username,'nickname':self.nickname,'password_hash':self.password_hash,'password_salt':self.password_salt,'status':self.status,'create_at':self.create_at.strftime('%Y-%m-%d %H:%M:%S'),'update_at':self.update_at.strftime('%Y-%m-%d %H:%M:%S')}

    class Meta:
        db_table = "user"  # 表名

class Blog(models.Model):
    nid=models.AutoField(primary_key=True)
    title=models.CharField(max_length=64)
    site_name=models.CharField(max_length=32)
    theme=models.CharField(max_length=64)
    def toDict(self):
        return {'title':self.title}
    class Meta:
        db_table="blog"

#分类表
class Category(models.Model):
    nid = models.AutoField(primary_key=True)
    title=models.CharField(max_length=64)
    blog=models.ForeignKey(to=Blog,to_field='nid',null=True,on_delete=models.CASCADE)
    def toDict(self):
        return {'title':self.title}
    class Meta:
        db_table="category"
#标签
class Tag(models.Model):
    nid = models.AutoField(primary_key=True)
    title=models.CharField(max_length=64)
    blog=models.ForeignKey(to=Blog,to_field='nid',null=True,on_delete=models.CASCADE)
    def toDict(self):
        return {'title':self.title}
    class Meta:
        db_table = "tag"  # 更改表名
#前端用户信息表
class Webuser(models.Model):
    nickname = models.CharField(max_length=50)
    head = models.CharField(max_length=255)
    mobile = models.CharField(max_length=50)
    password = models.CharField(max_length=50,null=True,blank=True)
    email = models.CharField(max_length=50)
    status = models.IntegerField(default=1)
    blog = models.OneToOneField(to=Blog,to_field='nid',null=True,on_delete=models.CASCADE)
    create_at = models.DateTimeField(default=datetime.now)
    update_at = models.DateTimeField(default=datetime.now)

    def toDict(self):
        return {'id':self.id,'blog':self.blog,'nickname':self.nickname,'head':self.head,'mobile':self.mobile,'head':self.head,'password':self.password,'status':self.status,'create_at':self.create_at.strftime('%Y-%m-%d %H:%M:%S'),'update_at':self.update_at.strftime('%Y-%m-%d %H:%M:%S')}

    class Meta:
        db_table = "webuser"  # 更改表名

#文章信息模型
class Article(models.Model):
    name = models.CharField(max_length=255)        #文章名称
    picture = models.CharField(max_length=255)  #封面图片
    main = models.CharField(max_length=255,null=True,blank=True)   #主要内容
    message = models.TextField()    #文章内容
    title = models.CharField(max_length=255)    #话题
    title_id = models.CharField(max_length=255)    #话题编号
    status = models.IntegerField(default=1)        #状态:1正常/2暂停/3删除
    publish_at = models.DateTimeField(default=datetime.now)    #发布时间
    up_num = models.IntegerField(default=0)                   #点赞数
    down_num = models.IntegerField(default=0)                     #收藏数
    blog = models.ForeignKey(to=Blog,to_field='nid',null=True,on_delete=models.CASCADE)
    category = models.ForeignKey(to=Category,to_field='nid',null=True,on_delete=models.CASCADE)
    tag = models.ManyToManyField(to=Tag , through='ArticleTOTag' , through_fields=('article','tag'))
    def toDict(self):
        articlename = self.name.split("-")
        return {'id':self.id,'name':articlename[0],'blog':self.blog,'category':self.category,'tag':self.tag,'picture':self.picture,'message':self.message,'title':self.title,'title_id':self.title_id,'status':self.status,'publish_at':self.publish_at.strftime('%Y-%m-%d %H:%M:%S'),'up_num':self.up_num,'webuser':self.webuser}

    class Meta:
        db_table = "article"  # 表名

class ArticleTOTag(models.Model):
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(to=Article,to_field='id',on_delete=models.CASCADE)
    tag = models.ForeignKey(to=Tag,to_field='nid',on_delete=models.CASCADE)


class Commit(models.Model):
    nid = models.AutoField(primary_key=True)
    webuser = models.ForeignKey(to='Webuser' , to_field='id',on_delete=models.CASCADE)
    article = models.ForeignKey(to='Article' , to_field='id',on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    publish_at = models.DateTimeField(default=datetime.now)
    parent = models.ForeignKey(to='self',to_field='nid',on_delete=models.CASCADE,null=True,blank=True)
    class Meta:
        db_table = "commit"  # 更改表名
#点赞
class UpAndDown(models.Model):
    nid = models.AutoField(primary_key=True)
    webuser = models.ForeignKey(to=Webuser,to_field='id',on_delete=models.CASCADE)
    article = models.ForeignKey(to=Article,to_field='id',on_delete=models.CASCADE)
    up_down = models.BooleanField()

    class Meta:
        unique_together=(("webuser","article"),)   #联合

#收藏
class Collect(models.Model):
    nid = models.AutoField(primary_key=True)
    webuser = models.ForeignKey(to=Webuser,to_field='id',on_delete=models.CASCADE)
    article = models.ForeignKey(to=Article,to_field='id',on_delete=models.CASCADE)
    up_down = models.BooleanField()

    class Meta:
        unique_together=(("webuser","article"),)   #联合

#个人简介及信息表
class Info(models.Model):
    id = models.AutoField(primary_key=True)
    webuser = models.ForeignKey(to='Webuser' , to_field='id' , on_delete=models.CASCADE)
    info = models.CharField(max_length=255)
    star = models.CharField(max_length=50)
    birth = models.DateTimeField(max_length=50,null=True)
    habit = models.CharField(max_length=255)
    school = models.CharField(max_length=127)
    location = models.CharField(max_length=127)

    class Meta:
        db_table = "info"  # 更改表名