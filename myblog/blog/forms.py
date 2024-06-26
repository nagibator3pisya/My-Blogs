import re

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordResetForm, \
    SetPasswordForm
from django.core.exceptions import ValidationError
from django_ckeditor_5.fields import CKEditor5Field
from django_ckeditor_5.widgets import CKEditor5Widget
from taggit.models import Tag

from blog.models import User, Article, Category, Comment


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'placeholder': 'Пароль'})
    )

    class Meta:
        model = User
        fields = ('username', 'password')

    def clean (self):
        cleaned_data = super().clean()
        return cleaned_data



class UserRegistrationForm(UserCreationForm):
    last_name = forms.CharField(max_length=20,min_length=3,widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Имя пользователя'}))

    first_name = forms.CharField(max_length=20,min_length=3,widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Фамилия пользователя'}))
    username = forms.CharField(max_length=20,min_length=5,widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Логин'}))
    email = forms.CharField(max_length=50,min_length=5,widget=forms.EmailInput(attrs={'class': 'form-control',
                                                           'placeholder': 'Введите адрес эл. почты'}))
    password1 = forms.CharField(max_length=20,min_length=8,widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Пароль'}))
    password2 = forms.CharField(max_length=20,min_length=8,widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Подтвердите пароль'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        error_messages = {
            'username': {
                'required': 'Логин обязателен.',
            },
            'last_name': {
                'required': 'Имя обязательно.',
            },
            'first_name': {
                'required': 'Фамилия обязательна.',
            },
            'email': {
                'required': 'Электронная почта обязательна.',
                'invalid': 'Введите действительный адрес электронной почты.',
            },
            'password1': {
                'required': 'Пароль обязателен.',
            },
            'password2': {
                'required': 'Повторите пароль.',
                'password_mismatch': 'Пароли не совпадают.',
            },
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Этот адрес электронной почты уже используется.')
        return email

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name and not last_name[0].isupper():
            raise ValidationError('Имя должно начинаться с заглавной буквы.')
        return last_name

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name and not first_name[0].isupper():
            raise ValidationError('Фамилия должна начинаться с заглавной буквы.')
        return first_name



    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 7:
            raise forms.ValidationError("Пароль должен содержать минимум 7 символов.")
        if not re.search(r'[A-Z]', password1):
            raise forms.ValidationError("Пароль должен содержать хотя бы одну заглавную букву.")
        if not re.search(r'[a-z]', password1):
            raise forms.ValidationError("Пароль должен содержать хотя бы одну строчную букву.")
        if not re.search(r'\d', password1):
            raise forms.ValidationError("Пароль должен содержать хотя бы одну цифру.")
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают.")
        return password2


class UserProfileForm(UserChangeForm):
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}), required=False)
    About_me = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Расскажите немного о себе, это же круто будет'
    }), required=False)
    Programming_skills = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите языки программирования через запятую'
    }), required=False)

    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'username', 'email', 'image', 'About_me', 'Programming_skills')

    def clean_Programming_skills(self):
        programming_skills = self.cleaned_data.get('Programming_skills')
        if programming_skills:
            if not re.match(r'^[\w\s,]+$', programming_skills):
                raise ValidationError('Пожалуйста, введите языки программирования, разделенные запятой.')
            skills_list = re.split(r'[,\s]+', programming_skills)
            cleaned_skills = [skill.strip() for skill in skills_list if skill]
            return ','.join(cleaned_skills)
        return ''


class UserForgotPasswordForm(PasswordResetForm):
    """
    Запрос на восстановление пароля
    """

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                
            })

    def clean_email(self):
        """
        Проверка, существует ли электронная почта в базе данных
        """
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            return email
        else:
            raise ValidationError("Пользователь с указанным адресом электронной почты не найден.")



class UserSetNewPasswordForm(SetPasswordForm):
    """
    Изменение пароля пользователя после подтверждения
    """

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                
            })



class ArticleCreateForm(forms.ModelForm):
    """
    Форма добавления статей на сайте
    """
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
        error_messages={'required': 'Пожалуйста, выберите категорию.'}
    )
    short_description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Краткое описание будет отображаться в новостной ленте'}),
        required=True,
        error_messages={'required': 'Пожалуйста, введите краткое описание.'},
        max_length=100
    )
    full_description = CKEditor5Field(
        verbose_name='Полное описание',
        config_name='extends'  # Указание конфигурации, если она отличается от стандартной
    )
    thumbnail = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        required=False
    )
    status = forms.ChoiceField(
        choices=Article.STATUS_OPTIONS,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
        error_messages={'required': 'Пожалуйста, выберите статус статьи.'}
    )
    tags = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите теги через запятую или пробел'}),
        required=False
    )

    class Meta:
        model = Article
        fields = ('title', 'category', 'short_description', 'full_description', 'thumbnail', 'status', 'tags')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Обновление атрибутов после инициализации формы
        self.fields['short_description'].widget.attrs.update({'class': 'form-control'})
        self.fields['full_description'].widget.attrs.update({'class': 'form-control django_ckeditor_5'})
        self.fields['short_description'].required = False
        self.fields['full_description'].required = False




class ArticleDraftUpdateForm(forms.ModelForm):
    """
    Форма для редактирования черновиков статей.
    """
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
        error_messages={'required': 'Пожалуйста, выберите категорию.'}
    )
    short_description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Краткое описание будет отображаться в новостной ленте'}),
        required=True,
        error_messages={'required': 'Пожалуйста, введите краткое описание.'}
    )
    full_description = CKEditor5Field(
        verbose_name='Полное описание',
        config_name='extends'  # Указание конфигурации, если она отличается от стандартной
    )
    thumbnail = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        required=False
    )
    status = forms.ChoiceField(
        choices=Article.STATUS_OPTIONS,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
        error_messages={'required': 'Пожалуйста, выберите статус статьи.'}
    )
    tags = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите теги через запятую'}),
        required=False
    )

    class Meta:
        model = Article
        fields = ('title', 'category', 'short_description', 'full_description', 'thumbnail', 'status', 'tags')


class ArticleUpdateForm(ArticleCreateForm):
    """
    Форма обновления статьи на сайте
    """
    tags = forms.CharField(label='Теги', max_length=1000, required=False)

    class Meta:
        model = Article
        fields = ArticleCreateForm.Meta.fields + ('updater', 'fixed')

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы под Bootstrap
        """
        tags = kwargs.pop('tags', '')  # Получаем строку тегов из аргументов
        super().__init__(*args, **kwargs)

        self.fields['fixed'].widget.attrs.update({
            'class': 'form-check-input'
        })

        # Применяем классы Bootstrap к полю для ввода тегов
        self.fields['tags'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите теги через запятую'
        })

        # Заполняем поле с тегами строкой из аргументов
        self.initial['tags'] = tags

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        if tags:
            # Преобразуем строку тегов в список
            tag_list = re.split(r'[,\s]+', tags)
            return ','.join(tag.strip() for tag in tag_list if tag.strip())
        return ''


class UserPasswordChangeForm(SetPasswordForm):
    """
    Форма изменения пароля
    """
    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })


class CommentCreateForm(forms.ModelForm):
    """
    Форма добавления комментариев к статьям
    """
    parent = forms.IntegerField(widget=forms.HiddenInput, required=False)
    content = forms.CharField(label='', widget=forms.Textarea(attrs={'cols': 30, 'rows': 5, 'placeholder': 'Комментарий', 'class': 'form-control'}))

    class Meta:
        model = Comment
        fields = ('content',)