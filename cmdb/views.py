from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, get_list_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse
from .models import *
import re
import datetime
import markdown
import json

# Create your views here.
def index(request):
    return HttpResponse("hello, i'm here")

def login(request):
    content = {}
    content["name"] = "luffy"
    # content["name"] = request.session['user']
    # return render(request,"hello.html",content)
    return  render(request,"login.html")

def Home(request):
    username = request.session['user']
    users = Users.objects.filter(name=username)
    user = users[0]
    # articles = Article.objects.filter(author=username)
    articles = Article.objects.all()
    content = {}
    content["user"] = user
    content["articles"] = articles
    user_articles = user.article_set.all()
    content['user_articles'] = user_articles
    # content['article_num'] = len(articles)

    return render(request, 'index.html', content)

def loginyanzheng(request):
    username = request.POST['name']
    password = request.POST['password']
    content = {}
    if username=="" or password=="":
        content['message'] = json.dumps("用户名或密码不能为空")
        content['status'] = json.dumps("fail")
        return render(request, 'login.html', content)
        # return HttpResponse("用户名或密码不能为空")
    else:
        user_serch = Users.objects.filter(name=username)
        if len(user_serch)==0:
            content['message'] = json.dumps("用户不存在")
            content['status'] = json.dumps("fail")
            return render(request, 'login.html', content)
            # return HttpResponse("用户不存在")
        if user_serch[0].password==password:
            request.session['user'] = username

            username = request.session['user']
            user = Users.objects.filter(name=username)
            # articles = Article.objects.filter(author=username)
            articles = Article.objects.all()

            content["user"] = user[0]
            content["articles"] = articles
            user_articles = user[0].article_set.all()
            content['user_articles'] = user_articles
            # content['article_num'] = len(articles)

            return render(request,'index.html', content)
        else:
            content['message'] = json.dumps("帐号不存在或密码错误")
            content['status'] = json.dumps("fail")
            return render(request, 'login.html', content)
            # return HttpResponse("登录失败")

def lognin(request):
    return render(request,"signin.html")

def register(request):
    content = {}
    if request.POST['user_name']=="" or request.POST["user_password"]=="":
        content['message'] = json.dumps("帐号密码不能为空")
        content['status'] = json.dumps("fail")
        return render(request, 'signin.html', content)
        # return HttpResponse("帐号密码不能为空")
    if request.POST['user_password']!=request.POST['user_password1']:
        content['message'] = json.dumps("两次密码输入不一致，请重新输入")
        content['status'] = json.dumps("fail")
        return render(request, 'signin.html', content)
        # return HttpResponse("两次密码输入不一致，请重新输入")

    username = request.POST['user_name']
    password = request.POST['user_password']
    newuser = Users(name=username,password=password)
    try:
        newuser.save(force_insert=True)
    except:
        content['message'] = json.dumps("帐号名已被注册，请重新注册")
        content['status'] = json.dumps("fail")
        return render(request, 'signin.html', content)
        # return HttpResponse("帐号名已被注册，请重新注册")
    request.session['user'] = username

    # username = request.session['user']
    user = Users.objects.filter(name=username)
    # articles = Article.objects.filter(author=username)
    articles = Article.objects.all()

    content["user"] = user[0]
    content["articles"] = articles
    user_articles = user[0].article_set.all()
    content['user_articles'] = user_articles
    # content['article_num'] = len(articles)
    return render(request, 'index.html', content)
    # return HttpResponse("帐号注册成功")

# def getArticle(request):
#     if request.session['user']==None:
#         render(request,'login.html',{'Message':"尚未登录，请登录后再请求文章"})
#
#     username = request.session['user']
#     articles = Article.objects.filter(author=username)
#     content={}
#     article_list = []
#     content["name"] = username
#     content["ariticles"] = articles
#     content['article_num'] = len(articles)
#     return render(request, 'hello.html', content)

def articleDetil(request, article_id):
    article_list = Article.objects.filter(id=article_id)
    obj = article_list[0]
    obj.views += 1
    obj.save()
    obj.body = markdown.markdown(obj.body, safe_mode='escape',
                                 extensions=[       ## 扩展模块
                                     'markdown.extensions.nl2br',
                                     'markdown.extensions.fenced_code',
                                     'markdown.extensions.sane_lists',
                                     'markdown.extensions.codehilite',
                                     'markdown.extensions.abbr',
                                     'markdown.extensions.attr_list',
                                     'markdown.extensions.def_list',
                                     'markdown.extensions.footnotes',
                                     'markdown.extensions.smart_strong',
                                     'markdown.extensions.meta',
                                     'markdown.extensions.tables'
                                 ])
    # content["article_detil"] = article_list[0]
    # content["article_detil"] = obj
    # content["name"] = request.session["user"]
    # print(markdown.markdown(obj.body))
    comments = obj.blogcomment_set.all().order_by("-created_time")   ## 外键反向匹配，通过文章查询对应的多个comment
    username = request.session['user']
    user = Users.objects.filter(name=username)
    content = {}
    content["user"] = user[0]
    content["article"] = obj
    content["comments"] = comments
    user_articles = user[0].article_set.all()
    content['user_articles'] = user_articles
    content['tags'] = obj.tags.all()
    # content["comment_num"] = len(comments)
    return render(request, 'detail.html', content)

def sortByTime(request):
    username=request.session['user']
    user = Users.objects.filter(name=username)
    # articles = Article.objects.filter(author=username)
    articles = Article.objects.all().order_by("-created_time")
    content = {}
    content["user"] = user[0]
    content["articles"] = articles
    user_articles = user.article_set.all()
    content['user_articles'] = user_articles
    # content['article_num'] = len(articles)
    return render(request, 'index.html', content)
    # return render(request, 'hello.html', content)

def sortByViews(request):
    username=request.session['user']
    user = Users.objects.filter(name=username)
    # articles = Article.objects.filter(author=username)
    articles = Article.objects.all().order_by("-views")
    content = {}
    content["user"] = user[0]
    content["articles"] = articles
    user_articles = user[0].article_set.all()
    content['user_articles'] = user_articles
    # content['article_num'] = len(articles)
    return render(request, 'index.html', content)


def choseByTime(request):
    year = int(request.GET['year'])
    month = int(request.GET['month'])
    articles = []
    article_list = Article.objects.all().order_by("created_time")
    # article_list = Article.objects.all().datetimes('created_time', 'month')
    for art in article_list:
        if art.created_time.year==year and art.created_time.month == month:
            articles.append(art)
    username=request.session['user']
    user = Users.objects.filter(name=username)
    # articles = Article.objects.filter(author=username)
    content = {}
    content["user"] = user[0]
    content["articles"] = articles
    user_articles = user[0].article_set.all()
    content['user_articles'] = user_articles
    return render(request, 'index.html', content)
    # return render(request, "hello.html", content)

def block_search(request):
    search_for = request.GET["search"]

    if search_for:
        result = []
        article_list = Article.objects.all()
        for article in article_list:
            if re.findall(search_for,article.title,flags=0):
                result.append(article)

        username = request.session['user']
        user = Users.objects.filter(name=username)
        # articles = Article.objects.filter(author=username)
        content = {}
        content["user"] = user[0]
        content["articles"] = result
        user_articles = user[0].article_set.all()
        content['user_articles'] = user_articles
        # content['article_num'] = len(result)

        return render(request, 'index.html', content)

        # return render(request, 'hello.html', {"article_search":result})

    else:
        return redirect('login')

# def

class ArticleView(ListView):
    template_name = "hello.html" ## 需要输出的模版
    context_object_name = "articles_list"   ## 指定模版中使用的上下文变量
    # model = Article    ## 指定数据来源

    def get_queryset(self):
        pass

    def get_context_data(self, *, object_list=None, **kwargs):

        pass




