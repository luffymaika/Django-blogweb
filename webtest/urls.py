"""webtest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from cmdb import views
from cmdb import Comment_views
from cmdb import view_change
from cmdb import view_blog

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',views.index),
    path('',views.login, name='login'),
    path(r'yanzheng/$',views.loginyanzheng, name='yanzheng'),## 验证接口
    path('register/',views.register, name = 'register'), ## 注册接口
    path('signin/',view_change.lognin, name='lognin'),##跳转注册界面
    path('home/', views.Home, name='home'),     ## 跳转首页
    path('login/', view_change.logout, name='logout'), ## 退出登录
    # path('getarticle/', views.getArticle, name='getarticle'), ## 获取文章列表
    ## URL可以通过named group方式传递指定参数，语法为： (?P<name>pattern)， name 可以理解为所要传递的参数的名称，pattern代表所要匹配的模式
    path('aritcle/(?P<article_id>\d+)/', views.articleDetil, name = 'detail'),
    path(r'search/', views.block_search, name='search'),       ## 搜索文章，返回文章列表页（主页）
    path('chosebytime/', views.choseByTime, name='chosebytime'),
    path('sortbytime/', views.sortByTime, name='sortbytime'),     ## 根据时间排序
    path('sortbyviews/', views.sortByViews, name='sortbyview'), ## 根据浏览量排序  ---------------
    path('article/(?P<article_id>\d+)/comment/', Comment_views.CommentView, name='comment'),    ## 进入文章详情页
    path('article/(?P<article_id>\d+)/write_comment/', Comment_views.addComment, name='add_comment'),   ## 添加文章评论，更新文章详情页  -------
    path('writeblog_page/', view_change.writeBlog, name='writeblog'),    ## 跳转撰写文章的页面
    path('writeblog/', view_blog.add_blog, name='addblog'), ## 保存撰写的文章      --------------
]
