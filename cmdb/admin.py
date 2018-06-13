from django.contrib import admin
from .models import *

# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title','author', 'category','created_time','last_modified_time')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','created_time','last_modified_time')

admin.site.register(Article,ArticleAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Tag)
admin.site.register(BlogComment)