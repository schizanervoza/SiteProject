from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate
from .models import Post


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Имя пользователя')
    password1 = forms.CharField(label=u'Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label=u'Повторите пароль', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.user = username
            return self.cleaned_data
        raise forms.ValidationError(u'Имя уже существует')

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 == password2:
            self.password = password1
            return self.cleaned_data
        else:
            raise forms.ValidationError(u'Пароли не совпадают')

    def get_user(self):
        return self.user or None

    def get_password(self):
        return self.password or None


class LoginForm(forms.Form):
    username = forms.CharField(label=u'Имя пользователя')
    password = forms.CharField(label=u'Пароль', widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        if not self.errors:
            user = authenticate(username=cleaned_data['username'], password=cleaned_data['password'])
            if user is None:
                raise forms.ValidationError(u'Имя пользователя и пароль не подходят')
            self.user = user
        return cleaned_data

    def get_user(self):
        return self.user or None

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text',)
    fake = forms.CharField(required=False,label='catch all spamers!!')