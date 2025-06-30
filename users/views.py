from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile
from django.contrib.auth.models import User
from django.http import HttpResponse

# New import for uploading image
import requests
from django.core.files.base import ContentFile


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Your account is now created! You are able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)


# ✅ REAL FINAL FIX: Overwrite image using Cloudinary URL upload
def force_upload_profile_image(request):
    try:
        user = User.objects.get(username="Ranveer")
        url = 'https://res.cloudinary.com/dbdqfgqti/image/upload/v1751310469/default_oygkle.jpg'
        response = requests.get(url)
        user.profile.image.save("default.jpg", ContentFile(response.content), save=True)
        return HttpResponse("✅ Cloudinary image has been saved to Ranveer's profile image field.")
    except Exception as e:
        return HttpResponse(f"❌ Error: {e}")
