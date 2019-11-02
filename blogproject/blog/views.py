from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse
from .models import Post, Category, Tag
from django.utils.text import slugify
import markdown
from markdown.extensions.toc import TocExtension
import re

def index(request):

    post_list = Post.objects.all()
#    return HttpResponse('欢迎大家来到我的博客！')
    return render(request, 'blog/index.html',context={
        # 'title' : '我的博客首页',
        # 'welcome' : '欢迎访问我的博客',
        'post_list' : post_list
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