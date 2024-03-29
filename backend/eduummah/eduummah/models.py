from django.contrib.auth.models import User
from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()  # This could be text, URL to an audio file, etc.

class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    progress = models.IntegerField(default=0)  # Example: percentage, points, etc.
    completed = models.BooleanField(default=False)
