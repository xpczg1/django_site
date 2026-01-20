# main/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Users


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label='Имя')
    last_name = forms.CharField(max_length=30, required=True, label='Фамилия')
    patronymic = forms.CharField(max_length=30, required=False, label='Отчество')

    class Meta:
        model = Users
        fields = ('username', 'first_name', 'last_name', 'patronymic', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.Name = self.cleaned_data['first_name']
        user.Surname = self.cleaned_data['last_name']
        user.Patronymic = self.cleaned_data['patronymic']

        # Автоматически назначаем роль "Пользователь"
        user.role = 'user'

        if commit:
            user.save()
        return user