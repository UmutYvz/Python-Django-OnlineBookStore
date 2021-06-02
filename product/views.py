from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
# Create your views here.
from product.models import Comment, CommentForm
from django.contrib.auth.decorators import login_required

def index(request):
    return HttpResponse("product page")


@login_required(login_url='/login')
def addcomment(request, id):
    url = request.META.get('HTTP_REFERER')  # get last url
    if (request.method == 'POST'):
        form = CommentForm(request.POST)
        if form.is_valid():
            current_user = request.user  # user info istek at
            data = Comment()
            data.user_id = current_user.id
            data.product_id = id
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, "Yorumunuz başarı ile gönderilmiştir. Teşekkür ederiz.")

            return HttpResponseRedirect(url)

    messages.warning(request, "Yorumunuz kaydedilemedi.")
    return HttpResponse("Kaydedilme İşlemi Gerçekleşmedi")
