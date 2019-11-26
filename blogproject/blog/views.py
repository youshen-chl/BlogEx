from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse
from .models import Post, Category, Tag
from django.utils.text import slugify
import markdown
from markdown.extensions.toc import TocExtension
import re
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):

    post_list = Post.objects.all()
<<<<<<< HEAD

    paginator = Paginator(post_list, 2) # 每页显示 25 个联系人
 
=======
#    return HttpResponse('欢迎大家来到我的博客！')
    paginator = Paginator(post_list, 8)

>>>>>>> 59cbee600d6a260295b6502489a8f0e2c0dbbb8f
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果用户请求的页码号不是整数，显示第一页
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果用户请求的页码号超过了最大页码号，显示最后一页
        contacts = paginator.page(paginator.num_pages)
<<<<<<< HEAD
 
    is_paginated = True if paginator.num_pages >= 2 else False

    return render(request, 'blog/index.html',context={
        'page_obj' : contacts,
        # 'is_paginated' : is_paginated,
        # 'paginator' : paginator,
        'currentPage'   : page,
        # 'listNum'   : ,
=======

    is_paginated = True if paginator.num_pages >= 2 else False

    return render(request, 'blog/index.html',context={
        # 'title' : '我的博客首页',
        # 'welcome' : '欢迎访问我的博客',
        'page_obj'  : contacts ,
        'is_paginated' : is_paginated ,
        'paginator' : paginator,
>>>>>>> 59cbee600d6a260295b6502489a8f0e2c0dbbb8f
    })

def category(request, pk):
    categy = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=categy)
    return render(request, 'blog/index.html',context={
        'post_list' : post_list
    })

def archive(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month)

    return render(request, 'blog/index.html',context={
        'post_list' : post_list
    })

def tags(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=tag)
    return render(request, 'blog/index.html',context={
        'post_list' : post_list
    })

def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    md = markdown.Markdown(extensions=[
                                        'markdown.extensions.extra',
                                        'markdown.extensions.codehilite',
                                        # 'markdown.extensions.toc',
                                        TocExtension(slugify=slugify),
                                    ])

    post.body = md.convert(post.body)

    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''
    # post.body = markdown.markdown(post.body,
    #                                 extensions=[
    #                                     'markdown.extensions.extra',
    #                                     'markdown.extensions.codehilite',
    #                                     'markdown.extensions.toc',
    #                                 ]) 
    return render(request,'blog/detail.html',context={'post' : post})


# from django.views.generic.list import ListView

# class IndexView(ListView):
#     model = Post
#     template_name = 'blog/index.html'
#     context_object_name = 'post_list'
#     # 指定 paginate_by 属性后开启分页功能，其值代表每一页包含多少篇文章
#     paginate_by = 2
