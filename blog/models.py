from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field
from taggit.managers import TaggableManager

MAX_IMAGE_SIZE = 5 * 1024 * 1024


def validate_image_size(value):
    """
    Membatasi ukuran gambar maksimal 5 MB.
    """
    if value and value.size > MAX_IMAGE_SIZE:
        raise ValidationError("Ukuran gambar maksimal 5 MB.")


class Post(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Judul",
    )

    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="Slug URL",
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="blog_posts",
        verbose_name="Penulis",
    )

    image = models.ImageField(
        upload_to="blog/%Y/%m/%d/",
        blank=True,
        null=True,
        validators=[validate_image_size],
        verbose_name="Gambar artikel",
    )

    tags = TaggableManager(
        verbose_name="Tag",
        blank=True,
    )

    meta_description = models.CharField(
        max_length=160,
        blank=True,
        help_text=(
            "Deskripsi SEO artikel, maksimal 160 karakter. "
            "Jelaskan isi dan manfaat artikel secara ringkas."
        ),
        verbose_name="Deskripsi SEO",
    )

    body = CKEditor5Field(
        "Isi Artikel",
        config_name="extends",
    )

    publish = models.DateTimeField(
        default=timezone.now,
        verbose_name="Tanggal publikasi",
    )

    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Tanggal dibuat",
    )

    updated = models.DateTimeField(
        auto_now=True,
        verbose_name="Terakhir diperbarui",
    )

    class Meta:
        ordering = ["-publish"]
        indexes = [
            models.Index(fields=["-publish"]),
        ]
        verbose_name = "Artikel"
        verbose_name_plural = "Artikel"

    def __str__(self):
        return self.title


class SiteSetting(models.Model):
    site_title = models.CharField(
        max_length=100,
        default="Dunia Kode",
        verbose_name="Judul situs",
    )

    site_tagline = models.CharField(
        max_length=255,
        default="Catatan Pemrograman Python & Django",
        verbose_name="Tagline situs",
    )

    footer_text = models.CharField(
        max_length=200,
        default="Hak Cipta Dilindungi.",
        verbose_name="Teks footer",
    )

    class Meta:
        verbose_name = "Pengaturan Situs"
        verbose_name_plural = "Pengaturan Situs"

    def __str__(self):
        return "Konfigurasi Utama Blog"
