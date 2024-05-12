from django.contrib import auth
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from blog.models import User
from blog.forms import UserLoginForm,UserRegistrationForm


def home(request):
    context = {'title': 'Мой блог'}
    return render(request, 'blog/index.html',context)
def logout_view(request):
    logout(request)
    return redirect('home')

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request,user)
                return  HttpResponseRedirect(reverse('home'))
    else:
       form = UserLoginForm()
    context = {'form': form, 'title': 'Вход'}
    return render(request, 'blog/login.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('home'))
    else:
        form = UserRegistrationForm()
    context = {'form': form , 'title': 'Регистрация'}
    return render(request, 'blog/register.html', context)


def profile(request):
    context = {'title':'Профиль'}
    return  render(request,'blog/user/profile.html' , context)





@csrf_exempt  # Use this decorator to exempt this view from CSRF verification
def accept_cookies(request):
    if request.method == 'POST':
        # Handle your logic here, such as setting a cookie
        response = JsonResponse({"status": "success"})
        response.set_cookie('cookie_consent', 'true')  # Example cookie setting
        return response
    return JsonResponse({"status": "error"}, status=400)