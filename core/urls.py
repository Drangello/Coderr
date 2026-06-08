from django.contrib import admin
from django.urls import include, path, re_path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from core.media import serve_media

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^api/media/(?P<path>.*)$', serve_media, name='media'),
    re_path(r'^media/(?P<path>.*)$', serve_media, name='legacy-media'),
    path('api/', include('auth_app.api.urls')),
    path('api/', include('profile_app.api.urls')),
    path('api/', include('offers_app.api.urls')),
    path('api/', include('orders_app.api.urls')),
    path('api/', include('reviews_app.api.urls')),
    path('api/', include('base_info_app.api.urls')),
] + staticfiles_urlpatterns()
