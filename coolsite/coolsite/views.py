from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    #return HttpResponse("This is the cool site index")
    return render(request, 'index.html')
