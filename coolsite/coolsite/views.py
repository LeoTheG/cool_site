from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django import forms
from django.shortcuts import render,redirect
from forms import UserRegistrationForm
#from django.core.exceptions import ValidationError

def index(request):
    #return HttpResponse("This is the cool site index")
    return render(request, 'index.html', {'user':request.user})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']
            password = cd['password']
            if not (User.objects.filter(username=username).exists()):
                print "Creating new user"
                user = User(username=username,password=password)
                user.save()
                login(request,user)
                return redirect('index')
            else:
                raise forms.ValidationError("That username already exists")
    else:
        form = UserRegistrationForm()
        return render(request, 'register.html', {'form':form,'user':request.user})
    return render(request, 'register.html', {'form':form,'user':request.user})
