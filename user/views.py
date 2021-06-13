from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from home.models import UserProfile, Setting
from product.models import Category


def index(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.filter(parent__isnull=False)
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {
        'category': category,
        'setting': setting,
        'profile': profile

    }
    return render(request, 'user_profile.html', context)
