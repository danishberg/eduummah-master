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

@api_view(['POST'])
def register_api(request):
    print("Received POST data:", request.data)  # This should now work as expected.
    form = CustomUserCreationForm(request.data)
    if form.is_valid():
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # Generate UID and token for email verification
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)

        current_site = get_current_site(request)
        activation_link = f"http://{current_site.domain}/verify-email/{uid}/{token}/"

        message = f"Hi,\n\nPlease click on the link to confirm your registration:\n{activation_link}\n\nThank you!"

        try:
            send_mail(
                'Activate your account.',
                message,
                'eduunoreply@gmail.com',
                [user.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Error sending email: {e}")
            return Response({'error': 'Email could not be sent. Please try again later.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'status': 'User created successfully. Check your email to verify.'}, status=status.HTTP_201_CREATED)
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

User = get_user_model()

def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        # Update is_active attribute to True
        user.is_active = True
        user.save()
        return HttpResponse('Your account has been activated successfully.')
    else:
        return HttpResponse('Invalid activation link or token.', status=400)





from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework import status


#from django.http import HttpResponse
#from django.views.decorators.csrf import csrf_exempt
#@csrf_exempt 

from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

@api_view(['POST'])
def login_api(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(username=email, password=password)

        if user and user.is_active and user.email_verified:
            login(request, user)
            return Response({'status': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials or account not verified.'}, status=status.HTTP_401_UNAUTHORIZED)










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
