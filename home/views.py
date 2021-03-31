from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

def index(request):
    text = "asdfasdf"
    context = {'text':text}
    return render(request,'index.html',context)