# blog/views.py
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator
from django.db.models import Q  # 1. Impor modul Q untuk pencarian kompleks
from taggit.models import (
    Tag,
)  # <-- WAJIB TAMBAHKAN: Impor model Tag dari library taggit


# OPTIMASI: Menambahkan parameter tag_slug dengan nilai default None agar fungsi ini multi-fungsi
def post_list(request, tag_slug=None):
    posts_list = Post.objects.all()
    tag = None  # Inisialisasi variabel tag aktif

    # 2. Ambil kata kunci pencarian dari URL parameter '?query='
    query = request.GET.get("query")
    if query:
        # Filter artikel: judul mengandung kata kunci ATAU isi mengandung kata kunci
        posts_list = posts_list.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        ).distinct()  # .distinct() memastikan tidak ada artikel ganda yang muncul

    # 3. LOGIKA BARU: Filter artikel berdasarkan tag yang diklik oleh pengunjung
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts_list = posts_list.filter(tags__in=[tag])

    # 4. Pagination tetap berjalan normal setelah hasil difilter
    paginator = Paginator(posts_list, 5)
    page_number = request.GET.get("page")
    posts = paginator.get_page(page_number)

    # 5. Kirimkan variabel 'posts', 'query', dan 'tag' ke template
    return render(
        request, "blog/post/list.html", {"posts": posts, "query": query, "tag": tag}
    )


def post_detail(request, year, month, day, post_slug):
    post = get_object_or_404(
        Post, slug=post_slug, publish__year=year, publish__month=month, publish__day=day
    )
    return render(request, "blog/post/detail.html", {"post": post})


def about(request):
    return render(request, "blog/about.html")
