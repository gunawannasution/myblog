# blog/context_processors.py
from .models import SiteSetting
from django.utils import timezone
from taggit.models import Tag
from .models import Post

def site_settings(request):
    # Mengambil baris data pengaturan pertama di database, jika belum ada, buat data default
    setting, created = SiteSetting.objects.get_or_create(id=1)
    return {"site_info": setting}

def sidebar_tags(request):
    published_posts = Post.objects.filter(publish__lte=timezone.now())

    tag_ids = published_posts.values_list("tags__id", flat=True).distinct()

    tags = Tag.objects.filter(id__in=tag_ids).order_by("name")

    return {
        "sidebar_tags": tags,
    }
