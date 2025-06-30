from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Profile


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account is now created! You are able to log in')
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
            messages.success(request, f'Your account has been updated')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, "users/profile.html", context)


# ✅ One-time profile image repair view
def fix_profile_images(request):
    default_url = 'https://res.cloudinary.com/dbdqfgqti/image/upload/v1751310469/default_oygkle.jpg'
    count = 0

    for profile in Profile.objects.all():
        image_str = str(profile.image)
        if not profile.image or image_str.strip() == "" or image_str.startswith("media/") or image_str.startswith("/media/"):
            profile.image = default_url
            profile.save()
            count += 1

    return HttpResponse(f"✅ Fixed {count} broken profile images.")
