from django.urls import path
from .views import record_progress, get_user_info, register, login_view

urlpatterns = [
    path('record-progress/', record_progress, name='record_progress'),
    path('user-info/', get_user_info, name='get_user_info'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
]
