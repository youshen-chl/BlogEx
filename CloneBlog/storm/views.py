from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from .models import Article

def hello(request):
    return HttpResponse('hello world!')

def showlist(request):
    return render(request, 'storm/index.html')

def shownav1(request):
    posts = Article.objects.all()
    return render(request, 'index_main.html', context={
        'posts' : posts,
    })

def shownav(request, bigslug, slug):
    return render(request, 'base_right.html')

def show_article(request, slug):
    pass