from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from order.models import ShopCartForm, ShopCart
from product.models import Category


def index(request):
    return HttpResponse("order app")


@login_required(login_url='/login')
def addtocart(request, id):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    checkProduct = ShopCart.objects.filter(product_id=id)  # ürün var mı yok mu kontrol
    if checkProduct:
        control = 1
    else:
        control = 0

    if (request.method == 'POST'):
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control == 1:
                data = ShopCart.objects.get(product_id=id)
                data.quantity += form.cleaned_data['quantity']
                data.save()
            else:
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id = id
                data.quantity = form.cleaned_data['quantity']
                data.save()
            messages.success(request, "Ürün sepete başarıyla eklendi.")
            return HttpResponseRedirect(url)

    else:
        if control == 1:
            data = ShopCart.objects.get(product_id=id)
            data.quantity += 1
            data.save()
        else:
            data = ShopCart()
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.save()
        messages.success(request, "Ürün sepete başarıyla eklendi.")
        return HttpResponseRedirect(url)

    messages.warning(request, "Ürünü sepete eklerken bir hata ile karşılaşıldı.")
    return HttpResponseRedirect(url)


@login_required(login_url='/login')
def shopcart(request):
    category = Category.objects.all()
    current_user = request.user
    sshopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in sshopcart:
        total += rs.product.price * rs.quantity

    context = {
        'shopcart': sshopcart,
        'category': category,
        'total': total
    }
    return render(request, 'shopcart_products.html', context)


@login_required(login_url='/login')
def deletefromcart(request, id):
    ShopCart.objects.filter(id=id).delete()
    messages.success(request, "Ürün başarı ile silinmiştir.")
    return HttpResponseRedirect("/shopcart")
