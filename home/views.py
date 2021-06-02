from django.shortcuts import render
from django.contrib import messages

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect

from home.models import Setting, ContactFormMessage, ContactFormu
from product.models import Product, Category, Images, Comment


def index(request):
    sliderData = Product.objects.all()[:5]
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    dailyProducts = Product.objects.all()[:4]
    lastProducts = Product.objects.all().order_by('-id')[:4]
    randomProducts = Product.objects.all().order_by('?')[:4]

    context = {'setting': setting,
               'page': 'home',
               'sliderdata': sliderData,
               'category': category,
               'dailyproducts': dailyProducts,
               'lastproducts': lastProducts,
               'randomproducts': randomProducts,
               }

    return render(request, 'index.html', context)


def aboutus(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()

    context = {'category': category, 'setting': setting, 'page': 'hakkımızda'}
    return render(request, 'aboutus.html', context)


def references(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()

    context = {'category': category, 'setting': setting, 'page': 'hakkımızda'}
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


def category_products(request, id, slug):
    category = Category.objects.filter(parent__isnull=False)
    products = Product.objects.filter(category_id=id)
    productsCount = Product.objects.filter(category_id=id).count()
    categoryData = Category.objects.get(pk=id)
    context = {'products': products,
               'category': category,
               'categorydata': categoryData,
               'count': productsCount}
    return render(request, 'products.html', context)


def product_detail(request, id, slug):
    category = Category.objects.all()
    comments = Comment.objects.filter(product_id=id)
    product = Product.objects.get(pk=id)
    images = Images.objects.filter(product_id=id)
    context = {
        'product': product,
        'category': category,
        'images': images,
        'comments': comments
    }

    return render(request, 'product_detail.html', context)
