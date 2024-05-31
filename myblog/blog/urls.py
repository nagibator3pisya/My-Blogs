from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from . import views
from .views import accept_cookies, logout_view, profile, UserForgotPasswordView, UserPasswordResetConfirmView, \
    ArticleByCategoryListView, ArticleDetailView, ArticleCreateView, cancel_article

from django.contrib.auth import views as auth_views





urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('blog/', views.blog, name='blog'),
    path('accept-cookies/', accept_cookies, name='accept-cookies'),
    path('logout/', logout_view, name='logout'),
    path('password-reset/', UserForgotPasswordView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='blog/email_v2/password_reset_done.html'), name='password_reset_done'),
    path('set-new-password/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('category/<str:slug>/', ArticleByCategoryListView.as_view(), name="articles_by_category"),
    path('articles/<str:slug>/', ArticleDetailView.as_view(), name='articles_detail'),
    path('articles/', ArticleCreateView.as_view(), name='articles_create'),
    path('articles/cancel/<int:pk>/', cancel_article, name='cancel_article'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
