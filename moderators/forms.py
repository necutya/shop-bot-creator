from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import forms as auth_forms


class ModeratorRegisterForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        label="Ім'я",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=30,
        label='Призвіще',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    username = forms.CharField(
        label='Логін',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label='Почтова адреса',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label="Підтвердження паролю",
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', "first_name", "last_name", 'password1', 'password2')


class ModeratorLoginForm(auth_forms.AuthenticationForm):
    """
    Add label and styles to default authentication form
    """
    username = forms.CharField(
        label='Логин',
        # widget=forms.TextInput(attrs={'class': 'main-form__field',
        #                               'autocomplete': "off"})
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'autocomplete': "off"})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'autocomplete': "off"})
    )


class ModeratorEditProfileForm(auth_forms.UserChangeForm):
    """
    Add label and styles to default UserChangeForm form
    """
    username = forms.CharField(
        label='Логін',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        label="Ім'я",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        label='Призвіще',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.CharField(
        label='Почтова адреса',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    password = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )

    class Meta:
        model = User
        fields = ('username',
                  'first_name',
                  'last_name',
                  'email')


class ModeratorChangePasswordForm(auth_forms.PasswordChangeForm):
    """
    Add label and styles to default PasswordChangeForm form
    """
    old_password = forms.CharField(
        label='Текущий пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    new_password1 = forms.CharField(
        label='Новий пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    new_password2 = forms.CharField(
        label='Подтверждение нового пароля',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
