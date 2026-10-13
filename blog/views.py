# blog/views.py
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator
from django.db.models import Q  # 1. Impor modul Q untuk pencarian kompleks [4]


def post_list(request):
    posts_list = Post.objects.all()

    # 2. Ambil kata kunci pencarian dari URL parameter '?query=' [1]
    query = request.GET.get("query")
    if query:
        # Filter artikel: judul mengandung kata kunci ATAU isi mengandung kata kunci [4]
        posts_list = posts_list.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        ).distinct()  # .distinct() memastikan tidak ada artikel ganda yang muncul [4]

    # 3. Pagination tetap berjalan normal setelah hasil difilter
    paginator = Paginator(posts_list, 5)
    page_number = request.GET.get("page")
    posts = paginator.get_page(page_number)

    # 4. Kirimkan juga variabel 'query' ke template agar kita bisa menampilkan teks "Hasil pencarian untuk..."
    return render(request, "blog/post/list.html", {"posts": posts, "query": query})


def post_detail(request, year, month, day, post_slug):
    post = get_object_or_404(
        Post, slug=post_slug, publish__year=year, publish__month=month, publish__day=day
    )
    return render(request, "blog/post/detail.html", {"post": post})


def about(request):
    return render(request,"blog/about.html")