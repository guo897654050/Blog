from ..models import Post, Category
from django import template

register = template.Library()

@register.simple_tag
def get_recent_posts(num=5):
    #获取数据库前num篇文章，num=5
    return Post.objects.all().order_by('-create_time')[:num]

@register.simple_tag
def archives():
    #data会返回一个列表，列表中元素是每一篇文章的创建时间，精确到月份，降序排列，最后一项代表降序排列
    return Post.objects.dates('create_time', 'month', order='DESC')

@register.simple_tag
def get_categories():
    return Category.objects.all()