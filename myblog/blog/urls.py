
from django.urls import path
from . import views
from .views import accept_cookies, logout_view,profile




urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('accept-cookies/', accept_cookies, name='accept-cookies'),
    path('logout/', logout_view, name='logout'),

]
