# blog/urls.py
from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    # 1. Halaman utama daftar artikel (Normal)
    path("", views.post_list, name="post_list"),
    
    # 2. RUTE BARU: Menangani filter otomatis saat tag diklik (Misal: /tag/python/)
    path("tag/<slug:tag_slug>/", views.post_list, name="post_list_by_tag"),
    
    # 3. Halaman detail artikel bawaan Anda
    path(
        "<int:year>/<int:month>/<int:day>/<slug:post_slug>/",
        views.post_detail,
        name="post_detail",
    ),
    
    # 4. Halaman tentang blog bawaan Anda
    path("about/", views.about, name="about"),
]
