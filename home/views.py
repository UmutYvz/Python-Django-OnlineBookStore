from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render
from django.contrib import messages

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect

import product
from home.models import Setting, ContactFormMessage, ContactFormu, UserProfile
from home.models import FAQ as sss
from order.models import ShopCart
from product.models import Product, Category, Images, Comment
from home.forms import SearchForm, SignUpForm
import json


def index(request):
    current_user = request.user

    sliderData = Product.objects.all()[:5]
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    dailyProducts = Product.objects.all()[:4]
    lastProducts = Product.objects.all().order_by('-id')[:4]
    randomProducts = Product.objects.all().order_by('?')[:4]
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()

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
    category = Category.objects.all()
    context = {'setting': setting, 'page': 'iletisim', 'form': form, 'category': category}
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
    commentCount = Comment.objects.filter(product_id=id).count()
    context = {
        'product': product,
        'category': category,
        'images': images,
        'comments': comments,
        'commentCount': commentCount
    }

    return render(request, 'product_detail.html', context)


def product_search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all()
            query = form.cleaned_data['query']
            products = Product.objects.filter(title__icontains=query)
            context = {
                'products': products,
                'category': category,
            }
            return render(request, 'products_search.html', context)

    return HttpResponseRedirect('/')


def product_search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        product = Product.objects.filter(title__icontains=q)
        results = []
        for rs in product:
            product_json = {}
            product_json = rs.title + " - " + rs.author
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "Giriş Başarısız. Bilgilerinizi Kontrol Ediniz.")
            return HttpResponseRedirect('/login')
    category = Category.objects.all()
    context = {
        'category': category,
    }
    return render(request, 'login.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.image = "images/users/user.png"
            data.save()
            messages.success(request, 'Üyelik işlemleriniz başarıyla tamamlandı.')
            return HttpResponseRedirect('/')

    form = SignUpForm()
    category = Category.objects.all()
    context = {
        'category': category,
        'form': form,
    }
    return render(request, 'signup.html', context)


def FAQ(request):
    category = Category.objects.all()
    faq = sss.objects.all().order_by('ordernumber')
    context = {
        'category': category,
        'faq': faq
    }
    return render(request, 'faq.html', context)
