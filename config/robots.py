from django.http import HttpResponse


def robots_txt(request):
    sitemap_url = request.build_absolute_uri("/sitemap.xml")

    content = (
        "User-agent: *\n" "Allow: /\n" "Disallow: /admin/\n" f"Sitemap: {sitemap_url}\n"
    )

    return HttpResponse(
        content,
        content_type="text/plain; charset=utf-8",
    )
