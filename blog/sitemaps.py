from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone

from .models import Post


class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = "https"

    def items(self):
        return Post.objects.filter(publish__lte=timezone.now()).order_by("-publish")

    def location(self, obj):
        return reverse(
            "blog:post_detail",
            kwargs={
                "year": obj.publish.year,
                "month": obj.publish.month,
                "day": obj.publish.day,
                "post_slug": obj.slug,
            },
        )

    def lastmod(self, obj):
        return obj.updated
