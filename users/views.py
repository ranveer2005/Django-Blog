from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Profile
from django.contrib.auth.models import User




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
    failed = []

    for profile in Profile.objects.all():
        img_path = str(profile.image or "").strip().lower()

        if (
            not img_path or
            img_path.startswith("media/") or
            img_path.startswith("/media/") or
            "profile_pics" in img_path or
            img_path.endswith(".jpg") or
            img_path.endswith(".jpeg")
        ):
            try:
                profile.image = default_url
                profile.save()
                count += 1
            except Exception as e:
                failed.append((profile.user.username, str(e)))

    return HttpResponse(f"✅ Fixed {count} profile images.<br>❌ Failed: {failed if failed else 'None'}")
def force_fix_specific_profile(request):
    default_url = 'https://res.cloudinary.com/dbdqfgqti/image/upload/v1751310469/default_oygkle.jpg'

    try:
        user = User.objects.get(username='Ranveer')  # change if needed
        profile = user.profile
        profile.image = default_url
        profile.save()
        return HttpResponse("✅ Successfully fixed Ranveer's profile image.")
    except Exception as e:
        return HttpResponse(f"❌ Failed to fix profile: {e}")
    
def show_raw_image_value(request):
    try:
        user = User.objects.get(username="Ranveer")  # ✅ change if needed
        image_value = str(user.profile.image)
        return HttpResponse(f"🧠 Image value in DB for Ranveer: <br><br><code>{image_value}</code>")
    except Exception as e:
        return HttpResponse(f"❌ Error: {e}")