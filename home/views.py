from django.shortcuts import render
from django.contrib import messages

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect

from home.models import Setting, ContactFormMessage, ContactFormu
from product.models import Product


def index(request):
    sliderData = Product.objects.all()[:5]
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting, 'page': 'home', 'sliderdata': sliderData}
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
    if request.method == 'POST':
        form = ContactFormu(request.POST)
        if form.is_valid():
            data = ContactFormMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, "Mesajınız başarı ile gönderilmiştir. Teşekkür ederiz.")
            return HttpResponseRedirect('/iletisim')

    setting = Setting.objects.get(pk=1)
    form = ContactFormu()
    context = {'setting': setting, 'page': 'iletisim', 'form': form}
    return render(request, 'contactus.html', context)
