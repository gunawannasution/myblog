# blog/admin.py
from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.decorators import display
from .models import Post, SiteSetting


@admin.register(Post)
class PostAdmin(ModelAdmin):
    list_display = ["title", "slug", "author", "show_publish"]
    list_filter = ["author", "created", "publish"]
    list_filter_submit = True
    search_fields = ["title", "body"]
    search_help_text = "Cari berdasarkan Judul atau Isi Konten Blog"
    prepopulated_fields = {"slug": ("title",)}

    # Konfigurasi tab kelompok pengisian field
    tab_groups = (
        (
            "Konten Utama",
            {
                "id": "tab-konten",
                "title": "Tulis Artikel",
                "fields": ["title", "slug", "author", "image", "body"],
            },
        ),
        (
            "Metadata & Publikasi",
            {
                "id": "tab-meta",
                "title": "Setelan & SEO",
                "fields": ["publish", "tags", "meta_keywords"],
            },
        ),
    )

    fieldsets = None

    # --- SUNTIKAN CSS TERBAIK DI SINI ---
    class Media:
        css = {
            "all": ("blog/css/custom_admin.css",)  # Memanggil file static kustom kita
        }

    # Fitur Badge Tanggal Terbit
    @display(description="Tanggal Terbit", label=True)
    def show_publish(self, obj):
        if obj.publish:
            return obj.publish.strftime("%d %b %Y, %H:%M"), "success"
        return "Belum Diterbitkan", "danger"


@admin.register(SiteSetting)
class SiteSettingAdmin(ModelAdmin):
    def has_add_permission(self, request):
        if SiteSetting.objects.exists():
            return False
        return True
