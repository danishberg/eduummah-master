from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import uuid
from django.core.mail import send_mail
from .models import CustomUser

# Ensure that CustomUserCreationForm is properly imported or defined
from .forms import CustomUserCreationForm
from .models import CustomUser, UserProgress, Lesson, Course  # Correctly import CustomUser
from .serializers import CourseSerializer, LessonSerializer, UserProgressSerializer

# You already import get_user_model, so you don't need to import it again
from django.contrib.auth.hashers import make_password
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator as token_generator

from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .forms import CustomUserCreationForm
from django.contrib.auth.hashers import make_password
import uuid

from rest_framework.decorators import api_view

# Token generator for the email confirmation
account_activation_token = PasswordResetTokenGenerator()

from rest_framework.decorators import api_view

from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .forms import CustomUserCreationForm
from verify_email.email_handler import send_verification_email

@api_view(['POST'])
def register_api(request):
    form = CustomUserCreationForm(request.data)
    if form.is_valid():
        inactive_user = send_verification_email(request, form)
        print(inactive_user.email)  # Just for checking; remove or secure this in production.
        print("Verification email sent. First stage complete")
        return Response({
            'status': 'User created successfully. Check your email to verify.'
        }, status=status.HTTP_201_CREATED)
    else:
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)




def record_progress(request):
    if not request.user.is_authenticated:
        return redirect('login')
    lesson = Lesson.objects.first()
    user_progress, created = UserProgress.objects.get_or_create(user=request.user, lesson=lesson)
    user_progress.progress += 1
    user_progress.save()
    return redirect('some_template_to_show_progress')

def get_user_info(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User is not logged in.'}, status=401)
    progress_items = UserProgress.objects.filter(user=request.user)
    total_progress = sum(item.progress for item in progress_items)
    user_info = {'username': request.user.username, 'email': request.user.email, 'total_progress': total_progress}
    return JsonResponse(user_info)



from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.urls import reverse

User = get_user_model()

@api_view(['POST'])
def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
#            user.email_verified = True  # Assuming you want to set email_verified to True
            #user.save() --- 02/04 TEST ATTENTION DO NOT FORGET TO EDIT THIS LINE - UTMOST IMPORTANCE - TESTING IN PROGRESS
            login_url = reverse('login')  # Use the name given to the URL pattern
            return HttpResponseRedirect(login_url)  # Redirect to the login page
        else:
            return HttpResponse('Invalid activation link or token.', status=400)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return HttpResponse('Invalid activation link.', status=400)


   






from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework import status


#from django.http import HttpResponse
#from django.views.decorators.csrf import csrf_exempt
#@csrf_exempt 

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login

from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view
from rest_framework.response import Response

import logging

# Set up basic configuration for logging
logger = logging.getLogger(__name__)

from django.contrib.auth import login, authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
def login_api(request):
    logger.info("Initiating login process.")
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None and user.is_active:
            login(request, user)
        #    request.session.save()

            logger.info(f"Session Key after login: {request.session.session_key}")
            logger.info(f"User Authenticated after login: {request.user.is_authenticated}")
            logger.info(f"Current User: {request.user.get_username()}")

        #    request.session['user_logged_in'] = True

            return Response({
                'status': 'Login successful', 
                'sessionKey': request.session.session_key,
                'email': user.email  # Sending user email to the frontend (if needed)
            }, status=status.HTTP_200_OK)
        
        else:
            logger.warning("Login failed: Invalid credentials or inactive account.")
            return Response({'error': 'Invalid credentials or account not verified.'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        logger.warning("login_api called with non-POST method.")
        return Response({'error': 'POST method required.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)





@api_view(['GET', 'POST'])
def logout_view(request):
    logout(request)
    return JsonResponse({'message': 'Logged out successfully'})

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
        return UserProgress.objects.filter(user=request.user)
    serializer_class = UserProgressSerializer


# Account Page Credentials Settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
import json

@csrf_exempt
def set_user_details(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')  # Assuming we're using email to identify the user
        name = data.get('name')
        surname = data.get('surname')
        dob = data.get('dob')

        User = get_user_model()
        try:
            user_profile = User.objects.get(email=email)
            if user_profile.details_set:
                return JsonResponse({'error': 'Account details can only be set once.'}, status=400)

            user_profile.name = name
            user_profile.surname = surname
            user_profile.date_of_birth = dob
            user_profile.details_set = True
            user_profile.save()

            return JsonResponse({'success': 'Account details updated successfully.'})
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found.'}, status=404)

    return JsonResponse({'error': 'Invalid request'}, status=400)


import logging

logger = logging.getLogger(__name__)

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def get_user_details(request):

    session_key_msg = f"Session ID: {request.session.session_key}" if hasattr(request.session, 'session_key') else "No Session Key"
    logger.info(session_key_msg)

    logger.info(f"Session ID: {request.session.session_key if hasattr(request.session, 'session_key') else 'No Session Key'}")
    logger.info(f"User Authenticated: {request.user.is_authenticated}")

    logger.info(f"Current User: {request.user.get_username()}")

    if request.user.is_authenticated:
        user_data = {
            'email': request.user.email,
            'name': request.user.first_name or '',
            'surname': request.user.last_name or '',
            'dob': str(request.user.profile.date_of_birth) if request.user.profile.date_of_birth else '',
        }
        return JsonResponse(user_data)
    else:
        return JsonResponse({'error': 'User is not authenticated'}, status=401)


