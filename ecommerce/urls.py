from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from store.views import create_admin_account

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
    path('make-me-admin-12345/', create_admin_account),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,  document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)