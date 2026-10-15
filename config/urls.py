# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap
from config.robots import robots_txt

sitemaps = {
    "posts": PostSitemap,
}
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("blog.urls", namespace="blog")),
    # TAMBAHKAN BARIS INI (Wajib untuk django-ckeditor-5)
    path("ckeditor5/", include("django_ckeditor_5.urls")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="sitemap",
    ),
    path(
        "robots.txt",
        robots_txt,
        name="robots_txt",
    ),
]

# urusan gambar nih
# Mengizinkan Django melayani file media saat masa development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
