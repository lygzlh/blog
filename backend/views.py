from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from django.views import View
from backend import models
from django import forms
from django.forms import widgets as w
from utils.page_list import Page
from utils.article_time import time_set
from django.utils.safestring import mark_safe
from utils.content_filter import filter
from django.db.models import Q
import json
import time

class baseResponse(object):
    '''
        返回值，后面以json格式返回
    '''
    def __init__(self):
        self.state = True
        self.data = None
        self.message = None


def jump(request):
    '''
    跳转到首页
    :param request:
    :return:
    '''
    return redirect('/home-1.html')

class userInfoForm(forms.ModelForm):
    class Meta:
        '''
            数据库的对象
        '''
        model = models.UserInfo
        fields = '__all__'
        labels = {
            'username':'用户名',
            'password':'密码'
        }
        widgets = {
            'username':w.Input(attrs={'id':'username','class':'form-control'}),
            'password':w.PasswordInput(attrs={'id':'password','class':'form-control'}),
        }


def logout(request):
    '''
    注销登录
    :param request:
    :return:
    '''
    request.session.clear()
    return redirect('/')

# Create your views here.
class homePage(View):
    '''
    首页
    '''
    def get(self,request,nid,cid,*args,**kwargs):
        res = {'is_login':None,'username':''}
        res['is_login'] = request.session.get('is_login', None)   #获取登录状态的session
        if res['is_login']:
            res['username'] = request.session.get('username')

        #获取数据库中文章的数据
        if not cid:
            article = models.Article.objects.all().order_by('-date')
        else:
            cid = int(cid)
            article = models.Article.objects.filter(category_id=cid).order_by('-date')
        if not nid:
            nid =0
        else:
            nid = int(nid)
        page = Page(nid, len(article), data_count=10)
        article = article[page.start():page.end()] #时间以最近发布排序
        a = page.list()
        time_set(article)
        return render(request,'homePage.html',{'res':res,'article':article,'a':a})


class login(View):
    def get(self,request,*args,**kwargs):
        '''
        接收get请求，跳转登录网页
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        obj = userInfoForm()
        return render(request,'login.html',{'result':obj})

    def post(self,request,*args,**kwargs):
        '''
        接收post请求，并对其做处理
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        rel = baseResponse()
        obj = userInfoForm(request.POST)
        if obj.is_valid():
            v = models.UserInfo.objects.filter(**obj.cleaned_data)
            if not v:
                rel.state = False
                return HttpResponse(json.dumps(rel.__dict__))
            request.session['username'] = obj.cleaned_data['username']
            request.session['author_id'] = v[0].id
            request.session['is_login'] = True
            request.session.set_expiry(0)
            return HttpResponse(json.dumps(rel.__dict__))
        else:
            print(obj.errors)
        return redirect('/login.html')


class register(View):
    '''
        注册管理
    '''
    def get(self,request,*args,**kwargs):
        '''
        处理get请求，返回注册页面
        :param requset:
        :param args:
        :param kwargs:
        :return:
        '''
        obj = userInfoForm()
        return render(request,'register.html',{'obj':obj})

    def post(self,request,*args,**kwargs):
        """
        处理用户填写的注册信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        base = baseResponse()
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username and not password:
            base.message = '用户名或密码不能为空'
            base.state = False
            return HttpResponse(json.dumps(base.__dict__))
        v = models.UserInfo.objects.filter(username=username)
        if v:
            base.state = False
            base.message = '用户名已存在'
        else:
            models.UserInfo.objects.create(username=username,password=password)
        return HttpResponse(json.dumps(base.__dict__))

class writeArticle(View):
    '''
    写博客和编辑
    '''
    def get(self,request,nid,*args,**kwargs):
        obj = models.Article.objects.filter(id=nid).first()
        return render(request,'writeArticle.html',{'obj':obj})

    def post(self,request,nid,*args,**kwargs):
        '''
        接收文章数据写入数据库
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        base = baseResponse()
        title = request.POST.get('title')
        introduce = request.POST.get('introduce')
        content = request.POST.get('content')
        content = filter(content)  #过滤一些非法语句
        category = request.POST.get('category')
        author_id = request.session.get('author_id')
        ticks = time.time()
        print(nid)
        if not nid:
            models.Article.objects.create(title=title,introduce=introduce,content=content,author_id=author_id,date=ticks,category_id=category)
        else:
            models.Article.objects.filter(id=nid).update(title=title,introduce=introduce,content=content,author_id=author_id,date=ticks,category_id=category)
        base.state = True
        return HttpResponse(json.dumps(base.__dict__))

class readArticle(View):
    '''
    读文章
    '''
    def get(self,request,nid,*args,**kwargs):
        obj = models.Article.objects.filter(id=nid).first()
        timeArray = time.localtime(obj.date)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        obj.date = otherStyleTime
        obj.content = mark_safe("".join(obj.content))

        return render(request,'readArticle.html',{'obj':obj})

class userCenter(View):
    '''
    用户中心
    '''
    def get(self,request,*args,**kwargs):
        return render(request,'userCenter.html')

class userInfo(View):
    '''
    用户信息
    '''
    def get(self,request,*args,**kwargs):
        obj = models.Article.objects.filter(author=request.session['author_id']).order_by('-date')
        return render(request,'userInfo.html',{'obj':obj})


def del_article(request,nid):
    '''
    删除用户的文章
    :param request:
    :return:
    '''
    models.Article.objects.filter(id=nid).delete()
    return redirect('user-info.html')

def search(request):
    '''
    搜索
    :param request:
    :return:
    '''
    text = request.GET.get('text')
    if not text:
        return redirect('/')
    rel = models.Article.objects.filter(title__contains=text)
    time_set(rel)
    return render(request,'search.html',{'article':rel})

class pswUpdate(View):
    '''
    修改密码
    :param request:
    :return:
    '''
    def get(self,request,*args,**kwargs):
        return render(request,'pwdUpdate.html')

    def post(self,request,*args,**kwargs):
        b = baseResponse()
        spwd = request.POST.get('spwd')
        cpwd = request.POST.get('cpwd')
        user = models.UserInfo.objects.filter(Q(username=request.session['username']),Q(password=spwd)).first()
        if user:
            user.password = cpwd
            user.save()
            b.state = True
            request.session.clear()
        else:
            b.state = False
        return HttpResponse(json.dumps(b.__dict__))