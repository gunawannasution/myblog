# blog/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field
from taggit.managers import TaggableManager
from django.core.exceptions import ValidationError
# validasi gambar dan ukurannya
def validate_image_size(value):
    max_size = 5 * 1024 * 1024  # 5 MB

    if value.size > max_size:
        raise ValidationError("Ukuran gambar maksimal 5 MB.")


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )

    # Kolom baru untuk gambar (bersifat opsional/boleh kosong agar postingan lama tidak error)
    image = models.ImageField(
        upload_to="blog/%Y/%m/%d/",
        blank=True,
        null=True,
        validators=[validate_image_size],
    )
    # --- FITUR BARU ---
    tags = TaggableManager()  # <-- 2. TAMBAHKAN MANAGER TAG
    # meta_keywords = models.CharField(
    #     max_length=255,
    #     blank=True,
    #     help_text="Pisahkan dengan koma, misal: django, python, tutorial",
    # )

    meta_description = models.CharField(
        max_length=160,
        blank=True,
        help_text=(
            "Deskripsi SEO artikel, maksimal 160 karakter. "
            "Jelaskan isi dan manfaat artikel secara ringkas."
        ),
    )
    # body = models.TextField()
    body = CKEditor5Field('Isi Artikel', config_name='extends')

    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-publish"]
        indexes = [
            models.Index(fields=["-publish"]),
        ]

    def __str__(self):
        return self.title

# buat configurasi utama nama blog dan deskripsi
class SiteSetting(models.Model):
    site_title = models.CharField(max_length=100, default="Dunia Kode")
    site_tagline = models.CharField(max_length=255, default="Catatan Pemrograman Python & Django"    )
    footer_text = models.CharField(max_length=200, default="Hak Cipta Dilindungi.")

    class Meta:
        verbose_name = "Pengaturan Situs"
        verbose_name_plural = "Pengaturan Situs"

    def __str__(self):
        return "Konfigurasi Utama Blog"
