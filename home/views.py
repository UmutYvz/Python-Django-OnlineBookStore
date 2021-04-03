from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

from home.models import Setting


def index(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting, 'page': 'home'}
    return render(request, 'index.html', context)


def aboutus(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting, 'page': 'hakkımızda'}
    return render(request, 'aboutus.html', context)


def references(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting, 'page': 'hakkımızda'}
    return render(request, 'references.html', context)


def contact(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting, 'page': 'iletişim'}
    return render(request, 'contactus.html', context)
