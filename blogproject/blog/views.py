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
    post_list_num = Post.objects.count()

    itemsOnPage = request.GET.get('itemsOnPage')
    if(not itemsOnPage):
        itemsOnPage = 10
    # print(itemsOnPage)
    paginator = Paginator(post_list, itemsOnPage) # 每页显示 10 个数据
 
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果用户请求的页码号不是整数，显示第一页
        contacts = paginator.page(1)
        page = 1
    except EmptyPage:
        # 如果用户请求的页码号超过了最大页码号，显示最后一页
        contacts = paginator.page(paginator.num_pages)
 
    is_paginated = True if paginator.num_pages > 1 else False
    # print(is_paginated)
    return render(request, 'blog/index.html',context={
        'page_obj' : contacts,
        'post_list_num' : post_list_num,
        'is_paginated' : is_paginated,
        'currentPage'   : page,
        'itemsOnPage'   : itemsOnPage,
    })

def category(request, pk):
    categy = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=categy)
    post_list_num = post_list.count()

    itemsOnPage = request.GET.get('itemsOnPage')
    if(not itemsOnPage):
        itemsOnPage = 10
    # print(itemsOnPage)
    paginator = Paginator(post_list, itemsOnPage) # 每页显示 10 个数据
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果用户请求的页码号不是整数，显示第一页
        contacts = paginator.page(1)
        page = 1
    except EmptyPage:
        # 如果用户请求的页码号超过了最大页码号，显示最后一页
        contacts = paginator.page(paginator.num_pages)
 
    is_paginated = True if paginator.num_pages >= 2 else False

    return render(request, 'blog/index.html',context={
        'page_obj' : contacts,
        'post_list_num' : post_list_num,
        'is_paginated' : is_paginated,
        'currentPage'   : page,
        'itemsOnPage'   : itemsOnPage,
    })

def archive(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month)

    post_list_num = post_list.count()

    itemsOnPage = request.GET.get('itemsOnPage')
    if(not itemsOnPage):
        itemsOnPage = 10
    # print(itemsOnPage)
    paginator = Paginator(post_list, itemsOnPage) # 每页显示 10 个数据
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果用户请求的页码号不是整数，显示第一页
        contacts = paginator.page(1)
        page = 1
    except EmptyPage:
        # 如果用户请求的页码号超过了最大页码号，显示最后一页
        contacts = paginator.page(paginator.num_pages)
 
    is_paginated = True if paginator.num_pages >= 2 else False

    return render(request, 'blog/index.html',context={
        'page_obj' : contacts,
        'post_list_num' : post_list_num,
        'is_paginated' : is_paginated,
        'currentPage'   : page,
        'itemsOnPage'   : itemsOnPage,
    })

def tags(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=tag)
    post_list_num = post_list.count()

    itemsOnPage = request.GET.get('itemsOnPage')
    if(not itemsOnPage):
        itemsOnPage = 10
    # print(itemsOnPage)
    paginator = Paginator(post_list, itemsOnPage) # 每页显示 10 个数据
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果用户请求的页码号不是整数，显示第一页
        contacts = paginator.page(1)
        page = 1
    except EmptyPage:
        # 如果用户请求的页码号超过了最大页码号，显示最后一页
        contacts = paginator.page(paginator.num_pages)
 
    is_paginated = True if paginator.num_pages >= 2 else False

    return render(request, 'blog/index.html',context={
        'page_obj' : contacts,
        'post_list_num' : post_list_num,
        'is_paginated' : is_paginated,
        'currentPage'   : page,
        'itemsOnPage'   : itemsOnPage,
    })

def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # 阅读量+1
    post.increase_views()

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
