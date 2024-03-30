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
        print("Received data:", request.data)
        form = CustomUserCreationForm(request.data)
        if form.is_valid():
            print("Form is valid")
            user = form.save(commit=False)
            user.is_active = False
            user.verification_token = uuid.uuid4()

            # Here, explicitly set the user's email field.
            # Assuming the form's 'username' field is used for the email address.
            user.email = request.data.get('username')

            user.save()
            print("User saved")

            verification_link = f"http://localhost:3000/verify/{user.verification_token}"
            print(f"Verification link: {verification_link}")

            # Now when you print this, it should show the email address.
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

@api_view(['POST'])
def login_api(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        print(f"Attempting to log in user: {username}")  # Debugging output
        user = authenticate(username=username, password=password)
        if user:
            print(f"User {username} authenticated. User active status: {user.is_active}")  # More debugging output
            if user.is_active:
                login(request, user)
                return Response({'status': 'Login successful.'}, status=status.HTTP_200_OK)
            else:
                print(f"User {username} is not active.")  # Debugging output for inactive user
                return Response({'error': 'Account is not activated.'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            print(f"Authentication failed for user: {username}")  # Debugging output for failed authentication
            return Response({'error': 'Invalid Credentials or Account Not Verified'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def verify_email(request, token):
    try:
        user = CustomUser.objects.get(verification_token=token, email_verified=False)
        print(f"User before activation: {user.email}, is_active: {user.is_active}")

        user.email_verified = True
        user.is_active = True
        user.verification_token = None
        user.save()

        # Re-fetch user from database to confirm changes were committed
        updated_user = CustomUser.objects.get(email=user.email)
        print(f"User after activation attempt: {updated_user.email}, is_active: {updated_user.is_active}")

        return Response({'status': 'Email verified successfully.'}, status=status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
        print("Verification failed: No such token")
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
