from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, get_list_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse
from .models import *
import re
import datetime
import markdown

# Create your views here.
def add_blog(request):
    blog = request.POST['blog']
    title = request.POST['title']
    user_name = request.session['user']
    choose_tags = request.POST['choose_tags']
    new_tags = request.POST['my_tags']
    choose_tags = choose_tags.strip()
    choose_tags = choose_tags.split()
    new_tags = new_tags.strip().split()
    print(new_tags)
    ## 新标签处理
    if(len(new_tags)>0):
        for tag in new_tags:
            newtag = Tag(name=tag, creator=user_name)
            newtag.save()

    print(choose_tags)
    status = 'p'
    # tag = Tag.objects.get(name = choose_tags[0])
    # print(len(tag))
    user_list = Users.objects.filter(name = user_name)
    user = user_list[0]
    newarticle = Article(title=title, author=user, body=blog, status=status)
    check = Article.objects.filter(title=title)
    if len(check)!=0:
        for article in check:
            if article.author.name==user_name:
                break
    else:
        try:
            newarticle.save()
            if len(choose_tags) > 0:
                for tag in choose_tags:
                    tag_object = Tag.objects.get(name=tag)
                    newarticle.tags.add(tag_object)
                    newarticle.save()
        except:
            return HttpResponse("文章创建出错了")



    # articles = Article.objects.filter(author=username)
    # articles = Article.objects.all()
    # content = {}
    # content["user"] = user
    # content["articles"] = articles
    # return  render(request, 'index.html', content)
    return HttpResponseRedirect('/home/')

def blok_search(request):
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