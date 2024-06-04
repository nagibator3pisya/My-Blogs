from django.contrib import auth, messages
from django.contrib.auth import logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from blog.forms import UserLoginForm, UserRegistrationForm, UserProfileForm, UserForgotPasswordForm, \
    UserSetNewPasswordForm, ArticleCreateForm, ArticleUpdateForm
from django.contrib.auth import login as auth_login

from blog.models import Article, Category

User = get_user_model()


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


# def profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(request.POST, request.FILES, instance=request.user)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('profile'))
#         else:
#             print(form.errors)
#     else:
#         form = UserProfileForm(instance=request.user)
#     context = {'title': 'Профиль', 'form': form}
#     return render(request, 'blog/user/profile.html', context)
#
#
# class ProfileView(TemplateView):
#     template_name = 'user/profile.html'
#
#     def get_context_data(self, *kwargs):
#         context = super().get_context_data(*kwargs)
#         context['username'] = self.request.user.username
#         context['first_name'] = self.request.user.first_name
#         context['drafts'] = Article.objects.filter(author=self.request.user)
#
#         return context
class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'blog/user/profile.html'
    success_url = reverse_lazy('profile')


    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['drafts'] = Article.objects.filter(author=self.request.user, status='draft')
        return context



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

    # def get_success_message(self, cleaned_data):
    #     # Используем self.request вместо request
    #     return messages.success(self.request, self.success_message, extra_tags='alert-success')




class ArticleByCategoryListView(ListView):
    model = Article
    template_name = 'blog/blog.html'
    context_object_name = 'articles'
    category = None

    def get_queryset(self):
        self.category = Category.objects.get(slug=self.kwargs['slug'])
        queryset = Article.objects.all().filter(category__slug=self.category.slug)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Статьи из категории: {self.category.title}'
        return context


# просмотр подробнее поста



class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/articles_detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        return context



class ArticleCreateView(CreateView):
    """
    Представление: создание материалов на сайте
    """
    model = Article
    template_name = 'blog/create_article/create_article.html'
    form_class = ArticleCreateForm
    success_url = reverse_lazy('blog')
    success_message = 'Пожалуйста, исправьте ошибки в форме.'



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление статьи на сайт'
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        if form.cleaned_data.get('status') == 'draft':
            messages.success(self.request, 'Статья сохранена как черновик.')
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)





class ArticleEditView(UpdateView):
    model = Article
    template_name = 'blog/create_article/articles_edit.html'
    form_class = ArticleUpdateForm



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Черновики'
        return context