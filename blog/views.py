from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.db.models import Count, Q
from taggit.models import Tag

from .models import Post, SiteSetting


def get_site_info():
    """
    Mengambil pengaturan situs.

    Jika belum ada konfigurasi yang tersimpan,
    template tetap dapat menggunakan nilai default.
    """
    return SiteSetting.objects.first()


def post_list(request, tag_slug=None):
    """
    Menampilkan daftar artikel yang sudah dipublikasikan.

    Mendukung:
    - Pencarian berdasarkan judul dan isi.
    - Filter artikel berdasarkan tag.
    - Pagination sebanyak 5 artikel per halaman.
    """

    now = timezone.now()

    posts_list = (
        Post.objects.filter(publish__lte=now)
        .select_related("author")
        .prefetch_related("tags")
        .order_by("-publish")
    )

    query = request.GET.get("query", "").strip()
    tag = None

    # Pencarian berdasarkan judul dan isi artikel.
    if query:
        posts_list = posts_list.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )

    # Filter berdasarkan tag.
    if tag_slug:
        tag = get_object_or_404(
            Tag,
            slug=tag_slug,
        )

        posts_list = posts_list.filter(
            tags__slug=tag_slug,
        ).distinct()

    # Pagination: 5 artikel per halaman.
    paginator = Paginator(posts_list, 5)
    posts = paginator.get_page(request.GET.get("page"))

    context = {
        "posts": posts,
        "query": query,
        "tag": tag,
        "site_info": get_site_info(),
    }

    return render(
        request,
        "blog/post/list.html",
        context,
    )


def post_detail(request, year, month, day, post_slug):
    """
    Menampilkan detail artikel yang sudah dipublikasikan.
    Artikel dicari berdasarkan slug dan tanggal publikasi.
    """

    now = timezone.now()

    post = get_object_or_404(
        Post.objects.filter(
            publish__lte=now,
        )
        .select_related("author")
        .prefetch_related("tags"),
        slug=post_slug,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )

    # Deskripsi SEO menggunakan deskripsi khusus jika tersedia.
    description = post.meta_description.strip() if post.meta_description else ""

    if not description:
        from django.utils.html import strip_tags
        from django.utils.text import Truncator

        description = Truncator(strip_tags(post.body)).chars(160)

    # URL absolut untuk canonical dan metadata sosial.
    canonical_url = request.build_absolute_uri(request.path)

    # Data JSON-LD untuk mesin pencari.
    import json

    structured_data = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": post.title,
        "description": description,
        "datePublished": post.publish.isoformat(),
        "dateModified": post.updated.isoformat(),
        "mainEntityOfPage": canonical_url,
        "author": {
            "@type": "Person",
            "name": post.author.get_username(),
        },
    }

    if post.image:
        structured_data["image"] = request.build_absolute_uri(post.image.url)

    structured_data_json = json.dumps(
        structured_data,
        ensure_ascii=False,
    ).replace("<", "\\u003C")

    context = {
        "post": post,
        "site_info": get_site_info(),
        "meta_description_text": description,
        "canonical_url": canonical_url,
        "structured_data_json": structured_data_json,
    }

    return render(
        request,
        "blog/post/detail.html",
        context,
    )


def about(request):
    """
    Menampilkan halaman Tentang.
    """

    context = {
        "site_info": get_site_info(),
    }

    return render(
        request,
        "blog/about.html",
        context,
    )


# BUAT ARTIKEL TERKAIT


def post_detail(request, year, month, day, post_slug):
    now = timezone.now()

    post = get_object_or_404(
        Post.objects.filter(publish__lte=now)
        .select_related("author")
        .prefetch_related("tags"),
        slug=post_slug,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )

    # Cari artikel lain berdasarkan tag yang sama.
    post_tags = post.tags.all()

    related_posts = (
        Post.objects.filter(
            publish__lte=now,
            tags__in=post_tags,
        )
        .exclude(pk=post.pk)
        .annotate(
            shared_tag_count=Count(
                "tags",
                filter=Q(tags__in=post_tags),
                distinct=True,
            )
        )
        .select_related("author")
        .prefetch_related("tags")
        .order_by("-shared_tag_count", "-publish")
        .distinct()[:3]
    )

    description = post.meta_description.strip() if post.meta_description else ""

    if not description:
        from django.utils.html import strip_tags
        from django.utils.text import Truncator

        description = Truncator(strip_tags(post.body)).chars(160)

    canonical_url = request.build_absolute_uri(request.path)

    import json

    structured_data = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": post.title,
        "description": description,
        "datePublished": post.publish.isoformat(),
        "dateModified": post.updated.isoformat(),
        "mainEntityOfPage": canonical_url,
        "author": {
            "@type": "Person",
            "name": post.author.get_username(),
        },
    }

    if post.image:
        structured_data["image"] = request.build_absolute_uri(post.image.url)

    structured_data_json = json.dumps(
        structured_data,
        ensure_ascii=False,
    ).replace("<", "\\u003C")

    context = {
        "post": post,
        "related_posts": related_posts,
        "site_info": get_site_info(),
        "meta_description_text": description,
        "canonical_url": canonical_url,
        "structured_data_json": structured_data_json,
    }

    return render(
        request,
        "blog/post/detail.html",
        context,
    )
