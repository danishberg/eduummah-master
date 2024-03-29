from django.urls import path, re_path, include
from django.views.generic import TemplateView
from . import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import logout_view

# Initialize the router and register the viewsets
router = DefaultRouter()
router.register(r'courses', views.CourseViewSet)
router.register(r'lessons', views.LessonViewSet)
# Correctly specify the basename for the UserProgressViewSet
router.register(r'userprogress', views.UserProgressViewSet, basename='userprogress')


urlpatterns = [
    # Django view routes
    path('record-progress/', views.record_progress, name='record_progress'),
    path('user-info/', views.get_user_info, name='get_user_info'),
    path('register_api/', views.register_api, name='register_api'),
    path('login_api/', views.login_api, name='login_api'),
    path('logout/', logout_view, name='logout'),

    # DRF viewset routes prefixed with 'api/'
    path('api/', include(router.urls)),

    # Catch-all pattern to serve index.html
    re_path(r'^(?:.*)/?$', TemplateView.as_view(template_name='index.html')),

    
]

# Serving static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
