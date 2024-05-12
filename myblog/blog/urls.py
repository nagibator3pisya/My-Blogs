
from django.urls import path
from . import views
from .views import accept_cookies

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('accept-cookies/', accept_cookies, name='accept-cookies'),
]
