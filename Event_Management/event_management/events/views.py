# events/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm,UserProfileForm
from django.contrib.auth.decorators import login_required
from .models import Event, Registration
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone

# registeration
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


# profile showing
@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})


# login with username and password
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# regsiter for an event
@login_required
def register_event(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        date = request.POST['date']
        location = request.POST['location']
        event = Event.objects.create(
            title=name,
            description=description,
            date=date,
            location=location
        )
        event.save()
        registration = Registration.objects.create(
            event=event,
            user=request.user,

        )
        registration.save()
        
        return redirect('dashboard')
    
    return render(request, 'register_event.html')

# bashboard
@login_required
def dashboard(request):
    current_date = timezone.now()
    registrations = Registration.objects.filter(user=request.user).select_related('event')

    # Filter past events directly using the ORM
    past_events = registrations.filter(event__date__lt=current_date)
    upcoming_events = registrations.filter(event__date__gte=current_date)

    return render(request, 'dashboard.html', {
        'past_events': past_events,
        'upcoming_events': upcoming_events
    })