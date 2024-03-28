from django.urls import path, re_path
from django.views.generic import TemplateView
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('record-progress/', views.record_progress, name='record_progress'),
    path('user-info/', views.get_user_info, name='get_user_info'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    # Add your API or other Django paths above this line

    # This line should be the last in the list:
    # It redirects any non-matching URL back to the index page, letting React handle the routing
    re_path(r'^(?:.*)/?$', TemplateView.as_view(template_name='index.html')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
