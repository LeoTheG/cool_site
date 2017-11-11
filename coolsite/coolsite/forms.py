from django import forms
from django.contrib.auth.models import User

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

    class Meta:
        model = User
        fields = ('username', 'password')

