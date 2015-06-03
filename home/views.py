from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
#    return HttpResponse("Hello World")
    print request.path
    return render(request, 'index.html')

def all(request):
    return render(request, request.path[1:])
