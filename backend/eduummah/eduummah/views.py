from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import UserProfile

def record_progress(request):
    # Logic for recording progress
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if the user is not logged in
    user_profile = UserProfile.objects.get(user=request.user)
    user_profile.progress += 1  # Increment progress
    user_profile.save()
    return redirect('some_template_to_show_progress')  # Placeholder redirect

def get_user_info(request):
    # Ensure the user is logged in
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User is not logged in.'}, status=401)

    # Fetch and return the user's profile info
    user_profile = UserProfile.objects.get(user=request.user)
    user_info = {
        'username': request.user.username,
        'email': request.user.email,
        'progress': user_profile.progress,
    }
    return JsonResponse(user_info)

def register(request):
    # Registration logic
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            UserProfile.objects.create(user=user)  # Create a profile on user registration
            login(request, user)
            return redirect('record_progress')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    # Login logic
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('record_progress')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})
