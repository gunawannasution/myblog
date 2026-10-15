# blog/dashboard.py
from django.utils.translation import gettext_lazy as _
from .models import Post


def get_dashboard_context(request, context):
    # Mengambil total data dari database untuk statistik (Metrics)
    total_posts = Post.objects.count()
    published_posts = Post.objects.filter(publish__isnull=False).count()
    draft_posts = total_posts - published_posts

    # Masukkan data kustom kita ke dalam dictionary context bawaan Unfold
    context.update(
        {
            # 1. Komponen Kartu Statistik (KPI Metrics)
            "kpi_metrics": [
                {
                    "title": _("Total Artikel"),
                    "value": total_posts,
                    "description": _("Semua artikel yang terdaftar"),
                    "icon": "article",  # Menggunakan Google Material Icons
                },
                {
                    "title": _("Sudah Terbit"),
                    "value": published_posts,
                    "description": _("Artikel yang live di blog"),
                    "icon": "check_circle",
                },
                {
                    "title": _("Draft / Pending"),
                    "value": draft_posts,
                    "description": _("Masih dalam tahap penulisan"),
                    "icon": "pending",
                },
            ],
            # 2. Komponen Informasi / Pengumuman Cepat
            "announcement": {
                "title": "Selamat Datang di Portal Blog Modern!",
                "message": "Gunakan tab di dalam artikel untuk mengelola konten dan metadata SEO dengan lebih terstruktur.",
            },
        }
    )

    # WAJIB: Kembalikan objek context yang sudah diperbarui
    return context
