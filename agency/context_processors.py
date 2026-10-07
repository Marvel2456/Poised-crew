from .models import SiteContent

def site_content(request):
    return {
        'site_content': SiteContent.get_solo()
    }
