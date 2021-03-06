from .models import Entry
from .models import Profile
from .models import Comment
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth import logout as logsout
from django.contrib.auth import login as logsin
from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
from django import forms
from forms import UserRegistrationForm
from forms import UserSignInForm
from forms import EntryForm

def get_entries(usernameslug):
    return list(User.objects.get(username=usernameslug).profile_set.first().entry_set.all())[::-1]

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
                profile = Profile(user=user)
                profile.save()
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
    if request.method == 'POST':
        print "user page:"+usernameslug
        user = User.objects.get(username=usernameslug)
        profile = user.profile_set.first()
        entry_set = profile.entry_set.all()
        for entry in entry_set:
            if ('comment-'+str(entry.id)) in request.POST:
                print "comment exists"
                commentBody = request.POST.get('comment-'+str(entry.id))[:128]
                c = Comment(body=commentBody,entry=Entry.objects.get(id=entry.id),user=request.user)
                print "Saving comment:"+commentBody+"\n\tfor entry:"+str(entry.id)
                c.save()

        '''
        for entry in User.objects.get(username=usernameslug).profile_set.first().entry_set().all():
            if request.POST['comment-'+str(entry.id)]:
                comment = request.POST['comment']
                c = Comment(body=comment,entry=Entry.objects.get(id=entry.id))
                print "Saving comment:"+comment+"\n\tfor entry:"+str(entry.id)
                c.save()
                '''
    return render(request, 'profile.html', {'usernameslug':usernameslug, 'user':request.user, 'entries':get_entries(usernameslug)})

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
        profile = User.objects.get(username=request.user.username).profile_set.first()
        #TODO check validity
        entry = Entry(title=title,body=body,profile=profile)
        entry.save()
        return redirect('user_profile',usernameslug=usernameslug)
        #return render(request, 'profile.html', {'usernameslug':usernameslug,'user':request.user,'form':form,'entries':get_entries(usernameslug)})
    return redirect('index')

def manage_posts(request, usernameslug):
    if not check_user_authentication(request,usernameslug):
        return redirect('index')
    if request.method == 'GET':
        return render(request, 'profile.html', {'usernameslug':usernameslug,'user':request.user,'entries':get_entries(usernameslug),'manage':True})
