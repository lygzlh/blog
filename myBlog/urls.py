"""myBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,re_path
from backend import views


urlpatterns = [
   # path('admin/', admin.site.urls),
    path('',views.jump),
    re_path('home-(?P<nid>\d+)(-(?P<cid>\d+))?.html', views.homePage.as_view()),     #主页
    path('login.html', views.login.as_view()),     #登录
    path('register.html', views.register.as_view()),     #注册
    path('logout', views.logout),     #注销
    path('search', views.search),     #搜索
    re_path('write-article(-(?P<nid>\d+))?.html', views.writeArticle.as_view()),     #写文章
    re_path('read/(?P<nid>\d+).html', views.readArticle.as_view()),     #读文章
    path('user-center.html', views.userCenter.as_view()),     #用户中心
    path('user-center/user-info.html', views.userInfo.as_view()),
    path('user-center/update-psw.html', views.pswUpdate.as_view()), #修改密码
    re_path('user-center/del_article-(?P<nid>\d+).html', views.del_article),    #删除文章
]
