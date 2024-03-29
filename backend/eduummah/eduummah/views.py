from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import User, UserProgress, Lesson, Course  # Include Course in the import
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import CourseSerializer, LessonSerializer, UserProgressSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from django.views.decorators.csrf import csrf_exempt


def record_progress(request):
    # Logic for recording user's progress in a specific lesson
    if not request.user.is_authenticated:
        return redirect('login')

    lesson = Lesson.objects.first()  # Example: Fetch the first lesson
    user_progress, created = UserProgress.objects.get_or_create(
        user=request.user, lesson=lesson
    )
    user_progress.progress += 1  # Example logic: Increment progress
    user_progress.save()
    
    return redirect('some_template_to_show_progress')

def get_user_info(request):
    # Ensure the user is logged in before providing information
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User is not logged in.'}, status=401)

    progress_items = UserProgress.objects.filter(user=request.user)
    total_progress = sum(item.progress for item in progress_items)

    user_info = {
        'username': request.user.username,
        'email': request.user.email,
        'total_progress': total_progress,
    }
    
    return JsonResponse(user_info)


from django.middleware.csrf import get_token

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .forms import CustomUserCreationForm

@api_view(['POST'])
def register_api(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.data)
        if form.is_valid():
            user = form.save()
            return Response({'status': 'User created successfully.'}, status=status.HTTP_201_CREATED)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_api(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            # Include CSRF token in response headers
            response = Response({'status': 'Login successful.'}, status=status.HTTP_200_OK)
            response['X-CSRFToken'] = get_token(request)
            return response
        else:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# Django Rest Framework viewsets

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class UserProgressViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # This method ensures that only user-specific progress data is returned.
        return UserProgress.objects.filter(user=self.request.user)
    
    serializer_class = UserProgressSerializer
