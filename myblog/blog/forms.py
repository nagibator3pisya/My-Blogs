import re

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordResetForm, \
    SetPasswordForm
from django.core.exceptions import ValidationError

from blog.models import User, Article, Category


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
    # коммитц если ничего не получится
    # def clean_password(self):
    #     password = self.cleaned_data.get('password')
    #     if not password:
    #         raise forms.ValidationError('Поле "Пароль" обязательно для заполнения.')
    #     return password


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

    class Meta:
        model = User
        fields = ('last_name','first_name', 'username','email', 'image')



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
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        required=True,
        error_messages={'required': 'Пожалуйста, введите краткое описание.'}
    )
    full_description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        required=True,
        error_messages={'required': 'Пожалуйста, введите полное описание.'}
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
    class Meta:
        model = Article
        fields = ('title', 'category', 'short_description', 'full_description', 'thumbnail', 'status')


class ArticleUpdateForm(forms.ModelForm):
    """
    Форма для редактирование в черновике
    """
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
        error_messages={'required': 'Пожалуйста, выберите категорию.'}
    )
    short_description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        required=True,
        error_messages={'required': 'Пожалуйста, введите краткое описание.'}
    )
    full_description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        required=True,
        error_messages={'required': 'Пожалуйста, введите полное описание.'}
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
    class Meta:
        model = Article
        fields = ('title', 'category', 'short_description', 'full_description', 'thumbnail', 'status')