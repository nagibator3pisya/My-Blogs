from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import accept_cookies, logout_view, ProfileView, UserForgotPasswordView, UserPasswordResetConfirmView, \
    ArticleByCategoryListView, ArticleDetailView, ArticleCreateView, ArticleEditView, ArticleDeleteView, \
    ArticleUpdateView, DraftsView, UserSettingsView, CommentCreateView, UserProfileView, LikeToggleView, article_list, \
    notifications, mark_all_notifications_as_read, mark_notification_as_read
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('blog/', views.blog, name='blog'),
    path('accept-cookies/', accept_cookies, name='accept-cookies'),
    path('logout/', logout_view, name='logout'),
    path('password-reset/', UserForgotPasswordView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='blog/email_v2/password_reset_done.html'),
         name='password_reset_done'),
    path('set-new-password/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('category/<str:slug>/', ArticleByCategoryListView.as_view(), name="articles_by_category"),
    path('articles/<str:slug>/', ArticleDetailView.as_view(), name='articles_detail'),
    path('articles/', ArticleCreateView.as_view(), name='articles_create'),
    path('drafts/', DraftsView.as_view(), name='drafts'),
    path('articles/<slug:slug>/edit/', ArticleEditView.as_view(), name='articles_edit'),
    path('articles/<str:slug>/update/', ArticleUpdateView.as_view(), name='articles_update'),
    path('articles/<int:pk>/delete/', ArticleDeleteView.as_view(), name='articles_delete'),
    path('settings/', UserSettingsView.as_view(), name='user_settings'),
    path('articles/<int:pk>/comments/create/', CommentCreateView.as_view(), name='comment_create_view'),
    path('profile/<str:username>/', UserProfileView.as_view(), name='user_profile'),
    path('like/', LikeToggleView.as_view(), name='like_toggle'),
    path('api/notifications/', views.notifications, name='notifications'),
    path('api/notifications/mark-all-read/', views.mark_all_notifications_as_read, name='mark_all_notifications_as_read'),
    path('api/notifications/<int:notification_id>/mark-read/', views.mark_notification_as_read, name='mark_notification_as_read'),
    path('show-more-notifications/', views.show_more_notifications, name='show_more_notifications'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
