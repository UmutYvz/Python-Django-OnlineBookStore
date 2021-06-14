from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from home.models import UserProfile, Setting
from product.models import Category
from user.forms import ProfileUpdateForm, UserUpdateForm


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


def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Hesabınız başarıyla güncellendi.')
            return redirect('/user')
    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        context = {
            'category': category,
            'user_form': user_form,
            'profile_form': profile_form,
        }
        return render(request, 'user_update.html', context)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Şifreniz başarıyla değiştirildi')
            return HttpResponseRedirect('/user')
        else:
            messages.error(request, 'Bir hata oluştu.<br>'+str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        return render(request, 'change_password.html', {
            'form': form,
            'category': category
        })
