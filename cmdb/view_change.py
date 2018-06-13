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

# Create your views here.

def writeBlog(request):
    username = request.session['user']
    user = Users.objects.filter(name=username)
    content = {}
    content["user"] = user[0]
    return render(request, 'write_blog.html', content)

def logout(request):
    del request.session['user']
    return render(request, 'login.html')

def lognin(request):
    return render(request,"signin.html")