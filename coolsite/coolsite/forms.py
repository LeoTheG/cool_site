from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class UserRegistrationForm(forms.Form):
    username = forms.CharField(
            required = True,
            label = 'Username',
            max_length = 32
            )
    password = forms.CharField(
            required = True,
            label= 'Password',
            max_length = 32,
            widget = forms.PasswordInput()
            )

    class Meta:
        model = User
        fields = ('username', 'password')
class UserSignInForm(forms.Form):
    username = forms.CharField(
            required = True,
            label = 'Username',
            max_length = 32
            )
    password = forms.CharField(
            required = True,
            label= 'Password',
            max_length = 32,
            widget = forms.PasswordInput()
            )

    def clean(self):
        cd = self.cleaned_data
        if authenticate(username=cd.get('username'),password=cd.get('password')) == None:
            self.add_error('password','incorrect password')
        return cd
    class Meta:
        model = User
        fields = ('username', 'password')

class EntryForm(forms.Form):
    title = forms.CharField(required=True, label='Title',max_length=32)
    body = forms.CharField(required=True, label='Post', max_length=1024)
