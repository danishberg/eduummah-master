# eduummah/backends.py
from django.contrib.auth.backends import ModelBackend
from .models import CustomUser  # Import CustomUser

class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        if email is None or password is None:
            return
        try:
            user = CustomUser.objects.get(email=email)  # Use CustomUser
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        except CustomUser.DoesNotExist:  # Catch the correct exception
            return None

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)  # Use CustomUser
        except CustomUser.DoesNotExist:  # Catch the correct exception
            return None


