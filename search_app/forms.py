from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.validators import EmailValidator


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        self.user = authenticate(username=username, password=password)
        if self.user is None:
            raise forms.ValidationError('Nieprawidlowy login i haslo')


def validate_login_free(username):
    try:
        check_user = User.objects.get(username=username)
        if check_user:
            raise forms.ValidationError("Użytkownik o danym loginie już istnieje")
    except Exception:
        pass


class UserForm(forms.Form):
    username = forms.CharField(max_length=64, label="Nazwa użytkownika", validators=[validate_login_free])
    password = forms.CharField(widget=forms.PasswordInput, label="Hasło")
    password_check = forms.CharField(widget=forms.PasswordInput, label="Wprowadź ponownie hasło")
    first_name = forms.CharField(max_length=64, label="Imię")
    last_name = forms.CharField(max_length=64, label="Nazwisko")
    email = forms.EmailField(label="email", validators=[EmailValidator])

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('password_check')

        if password1 != password2:
            raise forms.ValidationError('Hasła nie sią identyczne')
