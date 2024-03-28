# backend/eduummah/eduummah/urls.py

from django.urls import path
from django.views.generic import TemplateView
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('record-progress/', views.record_progress, name='record_progress'),
    path('user-info/', views.get_user_info, name='get_user_info'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
