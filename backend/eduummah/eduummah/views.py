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


@api_view(['POST'])
def register_api(request):
    print("Register API called")
    if request.method == 'POST':
        print("Received data:", request.data)  # Log received data
        form = CustomUserCreationForm(request.data)
        if form.is_valid():
            print("Form is valid")  # Confirm form validation.
            user = form.save(commit=False)
            user.is_active = False
            user.verification_token = uuid.uuid4()
            user.save()
            print("User saved")  # Confirm user saving.

            verification_link = f"http://localhost:3000/verify/{user.verification_token}"
            print(f"Verification link: {verification_link}")  # Log the verification link.

            print("Attempting to send verification email...")
            try:
                send_mail(
                    'Verify your email',
                    f'Please click on the link to verify your email: {verification_link}',
                    'eduunoreply@gmail.com',
                    [user.email],
                    fail_silently=False,
                )
                print("Email sending function executed.")
            except Exception as e:
                print(f"Error sending email: {e}")  # Catch and log any email sending errors.

            print("Verification email should have been printed above.")
            return Response({'status': 'User created successfully. Check your email to verify.'}, status=status.HTTP_201_CREATED)
        else:
            print("Form is invalid")  # Log form validation failure.
            print(form.errors)
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

@api_view(['POST'])
def login_api(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user and user.is_active:
            login(request, user)
            response = Response({'status': 'Login successful.'}, status=status.HTTP_200_OK)
            response['X-CSRFToken'] = get_token(request)
            return response
        else:
            return Response({'error': 'Invalid Credentials or Account Not Verified'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def verify_email(request, token):
    try:
        user = CustomUser.objects.get(verification_token=token, email_verified=False)
        user.email_verified = True
        user.is_active = True
        user.verification_token = None
        user.save()
        return Response({'status': 'Email verified successfully.'}, status=status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
        return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)

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
