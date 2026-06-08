"""Views for uploaded media files."""

from django.conf import settings
from django.views.static import serve


def serve_media(request, path):
    """Serve user uploads from the configured media volume."""
    return serve(request, path, document_root=settings.MEDIA_ROOT)
