from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def hello(request):
    return HttpResponse('hello world!')

def showlist(request):
    return render(request, 'storm/index.html')

def shownav(request):
    return render(request, 'base.html')