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
from cmdb import views

# Create your views here.
## 测试用例
def CommentView(request, article_id):
    if request.session['user']==None:
        render(request, 'login.html', {'Message': "尚未登录，请登录后再请求文章"})
    if request.POST['comment']=="":
        return HttpResponse("请填写了再进行评论")
    user_name = request.session['user']
    body = request.POST['comment']
    article_ = Article.objects.filter(id=article_id)
    user_ = Users.objects.filter(name=user_name)
    # newcomment = BlogComment(user_name=user_[0], body = body, article=article_[0])
    # newcomment.save()
    try:
        newcomment = BlogComment(user_name=user_[0], body=body, article=article_[0])
        newcomment.save()
        return HttpResponse("更新成功")
    except:
        return HttpResponse("出现了错误")

def addComment(request, article_id):
    comment = request.POST['comment']
    user_name = request.session['user']
    article_list = Article.objects.filter(id=article_id)
    user_list = Users.objects.filter(name= user_name)
    blogcomments = BlogComment.objects.filter(body=comment).filter(article = article_list[0]).filter(user_name=user_list[0])
    if len(blogcomments)>=1  :
        return views.articleDetil(request, article_id)
    newcomment = BlogComment(user_name=user_list[0], body = comment, article=article_list[0])
    try:
        newcomment.save()
    except:
        return HttpResponse("评论保存出错了")

    return views.articleDetil(request, article_id)
