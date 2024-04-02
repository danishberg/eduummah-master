from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class CustomUser(AbstractUser):
    email_verified = models.BooleanField(default=True)
    email = models.EmailField('email address', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # 'username' is not required, nor listed here

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = uuid.uuid4().hex  # Assign a unique value
        super().save(*args, **kwargs)



# Course model definition
class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

# Lesson model definition
class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()

# UserProgress model definition
class UserProgress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_progresses')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    progress = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
