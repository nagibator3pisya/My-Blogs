from django.contrib import auth
from django.http import JsonResponse
from django.shortcuts import render,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from blog.models import User
from blog.forms import UserLoginForm


def home(request):

    return render(request, 'blog/index.html')


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
    context = {'form': form}
    return render(request, 'blog/login.html', context)


def register(request):
    pass



@csrf_exempt  # Use this decorator to exempt this view from CSRF verification
def accept_cookies(request):
    if request.method == 'POST':
        # Handle your logic here, such as setting a cookie
        response = JsonResponse({"status": "success"})
        response.set_cookie('cookie_consent', 'true')  # Example cookie setting
        return response
    return JsonResponse({"status": "error"}, status=400)