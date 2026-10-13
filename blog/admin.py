# blog/admin.py
from django.contrib import admin
from .models import Post
from .models import SiteSetting


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "author", "publish"]
    list_filter = ["author", "created", "publish"]
    search_fields = ["title", "body"]
    prepopulated_fields = {"slug": ("title",)}


# blog/admin.py
@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    # Membatasi agar admin tidak bisa membuat banyak konfigurasi (cukup 1 baris data saja)
    def has_add_permission(self, request):
        if SiteSetting.objects.exists():
            return False
        return True
