def custom_settings(request):
    """Expose STATIC_BASE_URL and MEDIA_URL to templates.
    """
    from django.conf import settings
    return {
        'STATIC_BASE_URL': settings.STATIC_BASE_URL,
        'MEDIA_URL': settings.MEDIA_URL,
    }
