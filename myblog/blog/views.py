import re

from django.contrib import auth, messages
from django.contrib.auth import logout, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from taggit.models import Tag

from blog.forms import UserLoginForm, UserRegistrationForm, UserProfileForm, UserForgotPasswordForm, \
    UserSetNewPasswordForm, ArticleCreateForm, ArticleUpdateForm, ArticleDraftUpdateForm, UserPasswordChangeForm, \
    CommentCreateForm
from django.contrib.auth import login as auth_login

from blog.mixins import ViewCountMixin
from blog.models import Article, Category, Comment, Rating, Like
from blog.modules.services.utils import get_client_ip

User = get_user_model()


class CanEditArticleMixin(UserPassesTestMixin):
    def test_func(self):
        article = self.get_object()  # Получаем объект статьи, который мы хотим редактировать
        return self.request.user == article.author  # Проверяем, является ли текущий пользователь автором статьи

    def handle_no_permission(self):
        # Обработка случая, когда у пользователя нет прав доступа
        # Можно вернуть 403 ошибку, перенаправление или что-то еще
        return HttpResponseForbidden('У вас нет прав на редактирование этой статьи')


class CanDeleteArticleMixin(UserPassesTestMixin):
    def test_func(self):
        article = self.get_object()
        user = self.request.user
        return user.is_superuser or user.groups.filter(name='Модераторы').exists() or article.author == user

    def handle_no_permission(self):
        return HttpResponseForbidden('У вас нет прав на удаление этой статьи')


def home(request):
    if request.user.is_authenticated:
        return redirect('blog')
    context = {'title': 'Мой блог'}
    return render(request, 'blog/index.html', context)



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
                auth.login(request, user)
                return HttpResponseRedirect(reverse('blog'))
    else:
        form = UserLoginForm()
    context = {'form': form, 'title': 'Вход'}
    return render(request, 'blog/login.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return HttpResponseRedirect(reverse('blog'))
    else:
        form = UserRegistrationForm()
    context = {'form': form, 'title': 'Регистрация'}
    return render(request, 'blog/register.html', context)


def blog(request):
    context = {'title': 'Новостной блог'}
    return render(request, 'blog/blog.html', context)




class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'blog/user/profile.html'
    context_object_name = 'user_profile'

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()

        programming_skills = user.Programming_skills.split(',') if user.Programming_skills else []
        user_articles = Article.objects.filter(author=user)

        context['title'] = 'Профиль'
        context['user_articles'] = user_articles
        context['programming_skills'] = programming_skills
        context['user_profile_username'] = f"@{user.username}"
        return context


class DraftsView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'blog/user/drafts.html'
    context_object_name = 'drafts'
    paginate_by = 4

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user, status='draft')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        drafts_list = self.get_queryset()

        # Пагинация
        paginator = Paginator(drafts_list, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            drafts = paginator.page(page)
        except PageNotAnInteger:
            drafts = paginator.page(1)
        except EmptyPage:
            drafts = paginator.page(paginator.num_pages)

        context['drafts'] = drafts
        context['title'] = 'Черновики'
        return context

    def post(self, request, *args, **kwargs):
        if 'delete_draft' in request.POST:
            draft_id = request.POST.get('delete_draft')
            draft = get_object_or_404(Article, id=draft_id, author=request.user)
            draft.delete()
            messages.success(request, 'Черновик был удален.')
            return redirect('drafts')
        return super().post(request, *args, **kwargs)





@csrf_exempt  # Use this decorator to exempt this view from CSRF verification
def accept_cookies(request):
    if request.method == 'POST':
        # Handle your logic here, such as setting a cookie
        response = JsonResponse({"status": "success"})
        response.set_cookie('cookie_consent', 'true')  # Example cookie setting
        return response
    return JsonResponse({"status": "error"}, status=400)


class UserForgotPasswordView(SuccessMessageMixin, PasswordResetView):
    """
    Представление по сбросу пароля по почте
    """
    form_class = UserForgotPasswordForm
    template_name = 'blog/email_v2/password_reset.html'


    subject_template_name = 'blog/email_v2/password_subject_reset_mail.txt'
    email_template_name = 'blog/email_v2/password_reset_mail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Запрос на восстановление пароля'
        return context



class UserPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    """
    Представление установки нового пароля
    """
    form_class = UserSetNewPasswordForm
    template_name = 'blog/email_v2/password_set_new.html'

    success_url = reverse_lazy('home')
    success_message = 'Пароль успешно изменен. Можете авторизоваться на сайте.'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Установить новый пароль'
        return context

    def get_success_message(self, cleaned_data):
        # Используем self.request вместо request
        return messages.success(self.request, self.success_message, extra_tags='alert-success')




class ArticleByCategoryListView(ViewCountMixin,ListView):
    # сам блог
    model = Article
    template_name = 'blog/blog.html'
    context_object_name = 'articles'
    category = None

    def get_queryset(self):
        self.category = Category.objects.get(slug=self.kwargs['slug'])
        # отчечет за ебаный чернвоик.
        queryset = Article.objects.filter(category__slug=self.category.slug, status='published')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Статьи из категории: {self.category.title}'
        return context



class UserSettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'blog/user/setting_user.html'
    profile_form_class = UserProfileForm
    password_form_class = UserPasswordChangeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'profile_form' not in context:
            context['profile_form'] = self.profile_form_class(instance=self.request.user)
        if 'password_form' not in context:
            context['password_form'] = self.password_form_class(user=self.request.user)
        context['title'] = 'Настройки аккаунта'
        context['setting_user'] = 'Ваши Данные'
        context['setting_password'] = 'Изменения пароля'
        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get('form_type') == 'profile_form':
            profile_form = self.profile_form_class(request.POST, request.FILES, instance=request.user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Ваши настройки были успешно обновлены.')
            else:
                messages.error(request, 'Пожалуйста, исправьте ошибки ниже.')
            return self.render_to_response(self.get_context_data(profile_form=profile_form))

        elif request.POST.get('form_type') == 'password_form':
            password_form = self.password_form_class(user=request.user, data=request.POST)
            if password_form.is_valid():
                user = password_form.save()
                messages.success(request, 'Ваш пароль был успешно изменён!')
                update_session_auth_hash(request, user)  # Обновляем сессию пользователя
                return redirect(self.get_success_url())
            else:
                messages.error(request, 'Пожалуйста, исправьте ошибки ниже.')
            return self.render_to_response(self.get_context_data(password_form=password_form))

        return self.render_to_response(self.get_context_data())

    def get_success_url(self):
        return reverse_lazy('blog')


class ArticleDetailView(ViewCountMixin,DetailView):
    model = Article
    template_name = 'blog/articles_detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        # добавить ещё и на главную страницу и по категориям
        context['form'] = CommentCreateForm
        return context


class ArticleCreateView(CreateView):
    model = Article
    template_name = 'blog/create_article/create_article.html'
    form_class = ArticleCreateForm
    success_url = reverse_lazy('blog')
    success_message = 'Статья успешно создана.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление статьи на сайт'
        return context

    def form_valid(self, form):
        article = form.save(commit=False)
        article.author = self.request.user

        # Установите статус в зависимости от переданного значения
        article.status = self.request.POST.get('status', 'draft')

        tags = form.cleaned_data.get('tags')
        article.save()
        if tags:
            tag_list = re.split(r'[,\s]+', tags)
            for tag in tag_list:
                tag = tag.strip()
                if tag:
                    tag_obj, created = Tag.objects.get_or_create(name=tag)
                    article.tags.add(tag_obj)
        messages.success(self.request, self.success_message)
        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)




class ArticleEditView(UpdateView):
    model = Article
    template_name = 'blog/create_article/articles_edit.html'
    form_class = ArticleDraftUpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактировать статью'
        return context

    def form_valid(self, form):
        article = form.save(commit=False)
        article.status = self.request.POST.get('status', 'draft')  # Устанавливаем статус из формы
        article.save()

        if article.status == 'published':
            messages.success(self.request, 'Статья была опубликована.')
            return redirect('articles_detail', slug=article.slug)
        else:
            messages.success(self.request, 'Черновик был сохранен.')
            return redirect('drafts')  # Замените 'drafts' на имя вашего URL-шаблона для черновиков

    def get_initial(self):
        initial = super().get_initial()
        tags = self.object.tags.values_list('name', flat=True)  # Получаем список имен тегов
        initial['tags'] = ', '.join(tags)  # Преобразуем список в строку
        return initial


class ArticleUpdateView(LoginRequiredMixin, CanEditArticleMixin, UpdateView):
    model = Article
    template_name = 'blog/articles_update.html'
    context_object_name = 'article'
    form_class = ArticleUpdateForm  # Используем только form_class
    success_message = 'Статья отредактирована'
    success_url = reverse_lazy('blog')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Обновление статьи: {self.object.title}'
        return context
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['tags'] = ', '.join(tag.name for tag in self.object.tags.all())
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.success(self.request, self.success_message)
        return super().form_valid(form)


    def test_func(self):
        # Проверка, является ли текущий пользователь администратором или автором статьи
        article = self.get_object()
        return self.request.user.is_superuser or self.request.user == article.author


class ArticleDeleteView(LoginRequiredMixin, CanDeleteArticleMixin, DeleteView):
    """
    Представление: удаления материала
    """
    model = Article
    success_url = reverse_lazy('blog')
    context_object_name = 'article'
    template_name = 'blog/articles_delete.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Удаление статьи: {self.object.title}'
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'status': 'success'})



class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentCreateForm

    def is_ajax(self):
        return self.request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    def form_invalid(self, form):
        if self.is_ajax():
            return JsonResponse({'error': form.errors}, status=400)
        return super().form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.article_id = self.kwargs.get('pk')
        comment.author = self.request.user
        comment.parent_id = form.cleaned_data.get('parent')
        comment.save()

        if self.is_ajax():
            return JsonResponse({
                'is_child': comment.is_child_node(),
                'id': comment.id,
                'author': comment.author.username,
                'parent_id': comment.parent_id,
                'time_create': comment.time_create.strftime('%Y-%b-%d %H:%M:%S'),
                'avatar': comment.author.get_avatar_url(),  # Используем метод get_avatar_url
                'content': comment.content,
                'get_absolute_url': comment.author.get_absolute_url()
            }, status=200)

        return redirect(comment.article.get_absolute_url())




class UserProfileView(DetailView):
    model = User
    template_name = 'blog/user/profile.html'
    context_object_name = 'user_profile'

    def get_object(self):
        username = self.kwargs.get("username")
        return get_object_or_404(User, username=username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()

        programming_skills = user.Programming_skills.split(',') if user.Programming_skills else []
        user_articles = Article.objects.filter(author=user)

        context['title'] = 'Профиль'
        context['user_articles'] = user_articles
        context['programming_skills'] = programming_skills
        context['user_profile_username'] = f"@{user.username}"
        return context


class LikeToggleView(View):

    def post(self, request, *args, **kwargs):
        article_id = request.POST.get('article_id')
        ip_address = get_client_ip(request)
        user = request.user if request.user.is_authenticated else None

        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Article not found'}, status=404)

        like, created = Like.objects.get_or_create(
            article=article,
            ip_address=ip_address,
            user=user,
        )

        if not created:
            like.delete()
            return JsonResponse({'status': 'unliked', 'like_count': article.get_like_count()})

        return JsonResponse({'status': 'liked', 'like_count': article.get_like_count()})
