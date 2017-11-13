from django.contrib.auth.models import User
from django.http import JsonResponse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth import logout as logsout
from django.contrib.auth import login as logsin
from django import forms
from django.shortcuts import render,redirect
from forms import UserRegistrationForm
from forms import UserSignInForm
from forms import EntryForm
from coolsite.models import Entry
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
                user = User.objects.create_user(username=username,password=password)
                logsin(request,user)
                return redirect('index')
    else:
        form = UserRegistrationForm()
        return render(request, 'register.html', {'form':form,'user':request.user})
    return render(request, 'register.html', {'form':form,'user':request.user})

def validate_username(request):
    username = request.GET.get('username', None)
    data = {
            'is_taken': User.objects.filter(username__iexact=username).exists()
            }
    if data['is_taken']:
        data['error_message'] = 'A user with this username already exists.'

    return JsonResponse(data)

def login(request):
    if request.method == 'GET':
        form = UserSignInForm()
        return render(request, 'registration/login.html', {'form':form,'user':request.user})
    elif request.method == 'POST':
        form = UserSignInForm(request.POST)
        #username = User.objects.get(username=request.POST['username']).username
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            logsin(request, user)
        else:
            print "not authenticated user in login"
            return render(request, 'registration/login.html', {'form':form,'user':request.user})
    return redirect('index')

def logout(request):
    logsout(request)
    return redirect('index')

def check_user_authentication(request, usernameslug):
    if not request.user.is_authenticated():
        return False
    if not User.objects.filter(username=usernameslug).exists():
        return False
    return True

def user_profile(request, usernameslug):
    if not check_user_authentication(request,usernameslug):
        return redirect('index')
    return render(request, 'profile.html', {'usernameslug':usernameslug, 'user':request.user})

def new_post(request, usernameslug):
    if not check_user_authentication(request,usernameslug):
        return redirect('index')
    if request.method == 'GET':
        form = EntryForm()
        return render(request, 'new_post.html', {'usernameslug':usernameslug, 'user':request.user, 'form':form})
    elif request.method == 'POST':
        form = EntryForm(request.POST)
        title = request.POST['title']
        body = request.POST['body']
        profile = User.objects.get(username=request.user.username)
        #TODO check validity
        entry = Entry(title=title,body=body,profile=profile)
        entry.save()
        return render(request, 'profile.html', {'usernameslug':usernameslug,'user':request.user,'form':form})
    return redirect('index')
