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
from django.core import serializers

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
    ## 读取前端数据
    username = request.POST['user_name']
    password = request.POST['user_password']
    # print(password)
    # print(request.POST['identity'])
    if request.POST['identity']=='2':
        ISBN = request.POST['publisher_ISBN']
        # print(ISBN)
        contact = request.POST['contact']
        newuser = Users(name=username, password=password, identity='e', contact_wey=contact, publishers_ISBN=ISBN)
    else:
        newuser = Users(name=username,password=password)
    # newuser.save(force_insert=True)
    try:
        newuser.save(force_insert=True)
    except:
        content['message'] = json.dumps("帐号名已被注册，请重新注册")
        content['status'] = json.dumps("fail")
        return render(request, 'signin.html', content)
        return HttpResponse("帐号名已被注册，请重新注册")
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
    publishers = User_atten.objects.filter(article_id=obj.id)
    article_tag = obj.tags.all()
    recom_art = recommend(article_tag)
    username = request.session['user']
    user = Users.objects.filter(name=username)
    content = {}
    content["user"] = user[0]
    content['identity'] = json.dumps(user[0].identity)
    content["article"] = obj
    content["comments"] = comments
    user_articles = user[0].article_set.all()
    content['user_articles'] = user_articles
    content['tags'] = article_tag
    content['publishers'] = serializers.serialize('json', publishers)
    content['recommend'] = recom_art

    if user[0].identity == 'e':
        inter = User_atten.objects.filter(article_id=obj.id).filter(flower_id=username)
        if len(inter)>0:    ## 已关注
            content['interest']=json.dumps(1)
        else:
            content['interest']=json.dumps(0)
    elif obj.author.name==username:
        inter = User_atten.objects.filter(article_id = obj.id)
        inter_json = []
        for interest in inter:
            dic = {"pub_name":interest.flower_id, "pub_tel":interest.flower_contact}
            inter_json.append(dic)
        # content['interest_man'] = serializers.serialize('json', inter)
        content['interest_man'] = json.dumps(inter_json)
        content['interest'] = json.dumps(0)
    else:
        inter = {}
        content['interest_man'] = json.dumps(inter)
        content['interest'] = json.dumps(0)
    # content["comment_num"] = len(comments)
    return render(request, 'detail.html', content)

def recommend(tags):            #tags：当前待推荐博客的标签
    blogs = Article.objects.all().order_by("-created_time")
    articles = []
    value = [0]*len(blogs)
    for i in range(len(blogs)):
        select_tags = blogs[i].tags.all()
        for x in range(len(select_tags)):
            for j in range(len(tags)):
                if tags[j].name == select_tags[x].name:
                    value[i] = value[i]+1
    value_pop = value.copy()
    for i in range(3):
        a = value.index(max(value_pop))
        b = value_pop.index(max(value_pop))
        articles.append(blogs[a])
        value_pop.pop(b)
    # print(value)
    # print(value_pop)
    # print(articles)
    return(articles[1:3])

def sortByTime(request):
    username=request.session['user']
    user = Users.objects.filter(name=username)
    # articles = Article.objects.filter(author=username)
    articles = Article.objects.all().order_by("-created_time")
    content = {}
    content["user"] = user[0]
    content["articles"] = articles
    user_articles = user[0].article_set.all()
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


def be_interest(request, article_id):
    # print("it's interested")
    interest = request.POST['is_interested']
    # print(interest)
    editor_name = request.session['user']
    user = Users.objects.filter(name=editor_name)
    if(user[0].identity=='w'):
        return HttpResponse()

    history = User_atten.objects.filter(article_id=article_id).filter(flower_id=editor_name)
    if len(history)>0:
        if interest=="1":
            pass
        if interest=="0":
            history.delete()
            return HttpResponse(json.dumps("你已经取消关注"), content_type='application/json')
    else:
        if interest=="0":
            pass
        if interest=="1":
            newintest = User_atten(article_id=article_id, flower_id=user[0].name, flower_contact=user[0].contact_wey)
            try:
                newintest.save()
            except Exception as e:
                HttpResponse("error:%s"%e)
    return HttpResponse(json.dumps("你已关注"), content_type='application/json')

class ArticleView(ListView):
    template_name = "hello.html" ## 需要输出的模版
    context_object_name = "articles_list"   ## 指定模版中使用的上下文变量
    # model = Article    ## 指定数据来源

    def get_queryset(self):
        pass

    def get_context_data(self, *, object_list=None, **kwargs):

        pass




