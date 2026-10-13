# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("blog.urls", namespace="blog")),
    # TAMBAHKAN BARIS INI (Wajib untuk django-ckeditor-5)
    path("ckeditor5/", include("django_ckeditor_5.urls")),
]

# urusan gambar nih
# Mengizinkan Django melayani file media saat masa development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
