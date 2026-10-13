# blog/context_processors.py
from .models import SiteSetting


def site_settings(request):
    # Mengambil baris data pengaturan pertama di database, jika belum ada, buat data default
    setting, created = SiteSetting.objects.get_or_create(id=1)
    return {"site_info": setting}
