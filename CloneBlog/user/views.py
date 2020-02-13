from django.shortcuts import render, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import loginForm, userForm, ProfileForm
from .models import Ouser
import re
# Create your views here.

@csrf_exempt
def loginView(request):
    context = {}
    if request.method == 'POST':
    #POST
        form = loginForm(request.POST)
        # next_to 表示登陆后要跳转的地址
        next_to = request.POST.get('next', '/')

        remember = request.POST.get('remember', 0)
        if form.is_valid():
            # 获取表单内容
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            context = {'username':username, 'password':password, 'next_to':next_to}

            # 验证用户名、密码
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)    #登入 ， 会吧用户id存入session中 ‘_auth_user_id'
                    
                    # 存入用户信息
                    request.session['username'] = username
                    request.session['uid'] = user.id 
                    request.session['nick'] = None
                    request.session['nid'] = None
                    reqs = HttpResponseRedirect(next_to)

                    if remember != 0:
                        reqs.set_cookie('username', username)
                    else:
                        reqs.set_cookie('username', '', max_age=-1)
                    return reqs
                else:
                    context['inactive'] = True
                    return render(request, 'account/login.html', context)
            else:
                # 验证失败
                context['error'] = True
                return render(request, 'account/login.html', context)

    else:
    # GET  
        next_to = request.GET.get('next', '/')
        context['next_to'] = next_to

    return render(request, 'account/login.html', context)

def logoutView(request):
    next_to = request.GET.get('next','/')
    if next_to == '':
        next_to = '/'
    logout(request)
    return HttpResponseRedirect(next_to)

@csrf_exempt
def registerView(request):
    context = {}
    if request.method == 'POST':
        form = userForm(request.POST)
        # next_to 表示登陆后要跳转的地址
        next_to = request.POST.get('next', '/')
        # print('post')
        if form.is_valid():
            # 获取表单内容
            # print('is_valid')
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            email = form.cleaned_data['email']
            context = {'username':username, 'password':password, 'email':email, 'next_to':next_to}
            
            lpassword = len(password)
            if lpassword<8 or lpassword>20:
                context['pwd_error'] = 'length'
                print('1')
                return render(request, 'account/signup.html', context)
            if password != password2:
                context['pwd_error'] = 'unequal'
                return render(request, 'account/signup.html', context)
            if password.isdigit():
                context['pwd_error'] = 'nums'
                return render(request, 'account/signup.html', context)
            

            lname = len(username)
            if lname < 5 or lname > 20:
                context['user_error'] = 'length'
                return render(request, 'account/signup.html', context)
            elif Ouser.objects.filter(username=username):
                context['user_error'] = 'exit'
                return render(request, 'account/signup.html', context)

            if not re.match('^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$', email):
                context['email_error'] = 'format'
                return render(request, 'account/signup.html', context)
            if Ouser.objects.filter(email=email):
                context['email_error'] = 'exit'
                return render(request, 'account/signup.html', context)

            user = Ouser.objects.create_user(username=username, password=password, email=email)

            return HttpResponseRedirect(next_to)
        # else:
        #     print(form)
    else:
    # GET  
        next_to = request.GET.get('next', '/account/login')
        context['next_to'] = next_to
        print(context)
    return render(request, 'account/signup.html', context)

@login_required
def profileView(request):
    return render(request, 'oauth/profile.html')