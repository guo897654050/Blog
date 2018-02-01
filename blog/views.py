from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post, Category, Tag
from comments.forms import CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.db.models import Q
import markdown
# Create your views here.

def index(request):
   #global post_lists
    post_list = Post.objects.all().order_by('-pk')
    paginator = Paginator(post_list,4)#每页显示4篇文章
    print(paginator)
    page = request.GET.get('page')#用户点击page
    try:
        contacts = paginator.page(page)
       # contacts = paginator.page(page).obejct_list
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    context = {
        #'post_list':post_lists,
        'contacts':contacts,
        }
    return render(request,'blog/index.html',context)

def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.increase_views()
    post.body = markdown.markdown(post.body,
                                  extensions = [
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])
    form = CommentForm()
    # 获取这篇 post 下的全部评论
    #posts = Post.objects.all().order_by('-create_time')
    posts = Post.objects.all().order_by('-pk')[:5]
    print(posts)
    comment_list = post.comment_set.all()
    # 将文章、表单、以及文章下的评论列表作为模板变量传给 detail.html 模板，以便渲染相应数据。
    context = {
        'post': post,
        'posts':posts,
        'form': form,
        'comment_list': comment_list
    }
    return render(request,'blog/detail.html',context=context)

#归档信息
def archives(request, year, month):
    post_list = Post.objects.filter(create_time__year = year,
                                    create_time__month = month,
                                    ).order_by('-pk')
    paginator = Paginator(post_list, 4)  # 每页显示4篇文章
    page = request.GET.get('page')  # 用户点击page
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    context = {
        'post_list': post_list,
        'contacts': contacts,
    }
    return render(request, 'blog/index.html', {'contacts':post_list})

#分类页面
def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-pk')
    paginator = Paginator(post_list, 4)  # 每页显示4篇文章
    print(paginator)
    page = request.GET.get('page')  # 用户点击page
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    context = {
        #'post_list': post_list,
        'contacts': contacts,
    }
    return render(request, 'blog/index.html', context)
#标签
def tag(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=tag).order_by('-pk')
    paginator = Paginator(post_list, 4)  # 每页显示4篇文章
    print(paginator)
    page = request.GET.get('page')  # 用户点击page
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    context = {
        #'post_list': post_list,
        'contacts': contacts,
    }
    return render(request, 'blog/index.html', context)

#search
def search(request):
    q = request.GET.get('q')
    error_msg = ''
    if not q:
        error_msg = "请输入关键词"
        return render(request, 'blog/index.html', {'error_msg':error_msg})
    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog/index.html',{'contacts':post_list,'error_msg':error_msg})

