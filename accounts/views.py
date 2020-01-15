from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.urls import reverse
from accounts.forms import ProfileForm, SignupForm
from django.contrib import messages
from app.forms import MessageForm
from accounts.models import Profile


def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(**form.cleaned_data)
            messages.info(request, f"Successfully created user: {user.username}")
            login(request, user)
            return redirect(reverse('accounts:edit-profile'))
        messages.error(request, 'Invalid input: Please fix the appropriate fields and try again.')

    else:
        form = SignupForm()

    return render(request, 'registration/signup.html', {
        'form': form
    })


@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.info(request, 'Profile updated.')
            return redirect(reverse('accounts:my-profile'))
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'registration/edit_profile.html', {'form': form})


@login_required
def view_profile(request, user_id=None):
    if not user_id:
        profile = request.user.profile
        own = True
    else:
        try:
            profile = Profile.objects.get(user_id=user_id)
            own = False
        except Profile.DoesNotExist:
            messages.error(request, 'Profile does not exist.')
            return redirect(reverse('home'))

    runs = profile.runningprofile_set.all()
    rides = profile.ridingprofile_set.all()
    workouts = profile.workoutprofile_set.all()

    if request.method == 'POST':
        data = {'sender': request.user.profile, 'recipient': profile, 'text': request.POST['text']}
        form = MessageForm(data)
        form.save()
        messages.info(request, f"Message sent to {profile}")
        return redirect(reverse('home'))

    form = MessageForm()

    return render(request, 'registration/view_profile.html', {
        'profile': profile,
        'runs': runs,
        'rides': rides,
        'workouts': workouts,
        'own': own,
        'form': form
    })
