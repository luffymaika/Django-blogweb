from django.db import models

# Create your models here.
class Test(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=20)

class Users(models.Model):
    STATUS = (
        ('w','writer'),
        ('e','editor'),
    )
    name = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=20)
    identity =models.CharField('身份',max_length=1, choices=STATUS, default='w')
    contact_wey = models.CharField('联系方式',max_length=20, default="none")
    publishers_ISBN = models.CharField('出版商名字', max_length=20, default="none")

class User_atten(models.Model):
    article_id = models.IntegerField('文章id')
    flower_id = models.CharField('关注人账户名',max_length=20)
    flower_contact = models.CharField('联系方式',max_length=20, default="none")
    status = models.SmallIntegerField('状态', default=1)
    create_time = models.DateTimeField('创建时间',auto_now_add=True)

class Article(models.Model):
    STATUS_CHOICES = (
        ('d', 'part'),
        ('p', 'Published'),
    )  # 文章的状态

    title = models.CharField('标题',max_length=32)
    # author = models.CharField('作者',max_length=16)
    author = models.ForeignKey('Users', on_delete=models.CASCADE)
    body = models.TextField('正文')
    created_time = models.DateTimeField('创建时间',auto_now_add=True)   ##auto_now_add是设置时间为添加时的时间

    last_modified_time = models.DateTimeField('修改时间',auto_now=True)

    status = models.CharField('文章状态', max_length=1, choices=STATUS_CHOICES)
    ## null:表示数据可为null，blank表示可以填写空字符串
    abstract = models.CharField('摘要',max_length=54,blank=True, null=True,
                                help_text = '可选项，若为空则摘取正文前54个字符作为摘要')

    # on_delete 当指向的表被删除时，将该项设为空
    category = models.ForeignKey('Category', verbose_name='分类',
                                 null=True,
                                 on_delete=models.SET_NULL)
    # 阅读量
    views = models.PositiveIntegerField('浏览量', default=0)
    # 点赞数
    likes = models.PositiveIntegerField('点赞数', default=0)
    # 标签云
    tags = models.ManyToManyField('Tag', verbose_name='标签集合', blank=True)

    def __str__(self):  ## 用于在admin管理平台上的显示
        return self.title


    class Meta:
        # Meta 包含一系列选项，这里的ordering表示排序, - 表示逆序
        # 即当从数据库中取出文章时，以文章最后修改时间逆向排序
        ordering = ['-last_modified_time']

    def get_absolute_url(self):

        pass

class Category(models.Model):
    """
    另外一个表,储存文章的分类信息
    文章表的外键指向
    """
    name = models.CharField('类名', max_length=20)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    """
    tag(标签云)对应的数据库
    """
    name = models.CharField('标签名', max_length=20)
    creator = models.CharField('创建者名字',max_length=20, null=True)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)

    def __str__(self):
        return self.name

class BlogComment(models.Model):
    # user_name = models.CharField('评论者名字', max_length=100)
    user_name = models.ForeignKey('Users',on_delete=True)
    body = models.TextField('评论内容')
    article = models.ForeignKey('Article', verbose_name='评论所属文章', on_delete=models.CASCADE)
    created_time = models.DateTimeField('评论发表时间', auto_now_add=True)


    def __str__(self):
        return self.body[:20]

class Commentreview(models.Model):
    comment_id = models.ForeignKey(BlogComment,on_delete=True)
    blog_id = models.ForeignKey(Article,on_delete=True)
    reviewer_id = models.ForeignKey(Users, on_delete=True)
    content = models.TextField("回复内容")
    reply_time = models.DateTimeField("回复时间",auto_now_add=True)

    def __str__(self):
        return self.content[:20]
