from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone

from taggit.models import Tag

from .models import Post


def post_list(request, tag_slug=None):
    # Hanya tampilkan artikel yang tanggal publikasinya sudah tiba.
    posts_list = (
        Post.objects.filter(publish__lte=timezone.now())
        .select_related("author")
        .prefetch_related("tags")
        .order_by("-publish")
    )

    tag = None

    # Pencarian artikel berdasarkan judul dan isi.
    query = request.GET.get("query", "").strip()

    if query:
        posts_list = posts_list.filter(
            Q(title__icontains=query)
            | Q(body__icontains=query)
        )

    # Filter artikel berdasarkan tag.
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts_list = posts_list.filter(tags__slug=tag_slug)

    # Pagination: 5 artikel per halaman.
    paginator = Paginator(posts_list, 5)
    posts = paginator.get_page(request.GET.get("page"))

    context = {
        "posts": posts,
        "query": query,
        "tag": tag,
    }

    return render(request, "blog/post/list.html", context)


def post_detail(request, year, month, day, post_slug):
    # Artikel hanya dapat dibuka publik setelah tanggal publikasinya tiba.
    post = get_object_or_404(
        Post.objects.filter(
            publish__lte=timezone.now()
        ).select_related("author").prefetch_related("tags"),
        slug=post_slug,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )

    return render(
        request,
        "blog/post/detail.html",
        {"post": post},
    )


def about(request):
    return render(request, "blog/about.html")
