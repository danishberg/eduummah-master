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

@api_view(['POST'])
def register_api(request):
    print("Register API called")
    if request.method == 'POST':
        print("Received data:", request.data)
        form = CustomUserCreationForm(request.data)
        if form.is_valid():
            print("Form is valid")
            user = form.save(commit=False)
            user.is_active = False
            user.verification_token = uuid.uuid4()

            # Explicitly set the user's email field.
            user.email = request.data.get('username')

            # Hash the password before saving the user
            user.password = make_password(request.data.get('password'))

            user.save()
            print("User saved")

            verification_link = f"http://localhost:3000/verify/{user.verification_token}"
            print(f"Verification link: {verification_link}")

            # Attempt to send verification email
            print(f"Attempting to send verification email to {user.email}...")
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
                print(f"Error sending email: {e}")

            print("Verification email should have been printed above.")
            return Response({'status': 'User created successfully. Check your email to verify.'}, status=status.HTTP_201_CREATED)
        else:
            print("Form is invalid")
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


@api_view(['GET'])
def verify_email(request, token):
    try:
        user = CustomUser.objects.get(verification_token=token)
        if not user.email_verified:
            user.email_verified = True
            user.is_active = True
            user.verification_token = None  # Clear the token after verification.
            user.save()

            # Confirm the update for debugging.
            print(f"Verification successful for {user.username}. Active: {user.is_active}, Email Verified: {user.email_verified}")
            return Response({'status': 'Email verification successful. Please log in.'}, status=status.HTTP_200_OK)
        else:
            # User is already verified.
            print(f"User {user.username} is already verified.")
            return Response({'error': 'Email already verified.'}, status=status.HTTP_400_BAD_REQUEST)
    except CustomUser.DoesNotExist:
        print("Invalid or expired token.")
        return Response({'error': 'Invalid or expired token.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def login_api(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        if user.is_active and user.email_verified:
            login(request, user)
            return Response({'status': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Account not activated or email not verified'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)




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
