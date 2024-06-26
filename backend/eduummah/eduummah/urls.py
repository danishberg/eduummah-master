from django.urls import path, include, re_path
from django.views.generic import TemplateView
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'courses', views.CourseViewSet)
router.register(r'lessons', views.LessonViewSet)
router.register(r'userprogress', views.UserProgressViewSet, basename='userprogress')

#Recent
from django.views.generic import TemplateView

urlpatterns = [
    path('record-progress/', views.record_progress, name='record_progress'),
    path('user-info/', views.get_user_info, name='get_user_info'),
    path('register_api/', views.register_api, name='register_api'),
    path('login_api/', views.login_api, name='login_api'),
    path('logout/', views.logout_view, name='logout'),
    path('verification/', include('verify_email.urls')),
    path('verify-email/<uidb64>/<token>/', views.verify_email, name='email-verify'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
 #   path('set_user_details/', views.set_user_details, name='set_user_details'),
    path('api/set_user_details', views.set_user_details, name='set_user_details'),
    path('api/retrieve_user_details/', views.retrieve_user_details, name='api/retrieve_user_details/'),
    path('check_session/', views.check_session, name='check_session'),
    path('check_auth_status/', views.check_auth_status, name='check_auth_status'),
    re_path(r'^.*', TemplateView.as_view(template_name='index.html'), name='app'),
]

urlpatterns = [
    path('login/', TemplateView.as_view(template_name='index.html'), name='login'),
] + urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
