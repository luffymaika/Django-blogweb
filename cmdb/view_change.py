from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, get_list_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse
from .models import *
import json
from django.core import serializers
import re
import datetime
import markdown

# Create your views here.

def writeBlog(request):
    username = request.session['user']
    user = Users.objects.filter(name=username)
    user_tags = Tag.objects.filter(creator = username)
    # user_tags_list = user_tags.values_list('name')
    # print(user_tags_list)
    content = {}
    content["user"] = user[0]
    content['user_tags'] = user_tags
    content['olduser_tags'] = serializers.serialize("json",user_tags)
    return render(request, 'write_blog.html', content)

def logout(request):
    # del request.session['user']
    request.session.clear()
    return render(request, 'login.html')

def lognin(request):
    return render(request,"signin.html")