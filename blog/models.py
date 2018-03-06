from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import markdown
from django.utils.html import strip_tags
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=70)
    body = models.TextField()#对应一段文本
    create_time = models.DateField()
    modified_time = models.DateField()#修改时间
    excerpt = models.CharField(max_length=200,blank=True)#文章摘要，其中Blank=True代表可以允许空值
    category = models.ForeignKey(Category)#规定一篇文章对应一个分类
    tags = models.ManyToManyField(Tag)#一篇文章可以有多个标签，一个标签下也可以有多个文章
    author= models.ForeignKey(User)
    views = models.PositiveIntegerField(default=0,null=True)

    def __str__(self):
        return self.title

    def save(self,*args,**kwargs):
        if not self.excerpt:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            self.excerpt = strip_tags(md.convert(self.body))[:54]
        super(Post,self).save(*args,**kwargs)

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk':self.pk})

