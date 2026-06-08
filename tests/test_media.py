from pathlib import Path

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
import pytest


@pytest.mark.django_db
def test_media_is_served_with_debug_disabled(
    api_client,
    create_customer,
    tmp_path,
):
    with override_settings(DEBUG=False, MEDIA_ROOT=tmp_path):
        user = create_customer('media_customer', 'password')
        user.profile.file.save(
            'avatar.gif',
            SimpleUploadedFile(
                'avatar.gif',
                b'GIF89a',
                content_type='image/gif',
            ),
        )

        response = api_client.get(
            f'/api/media/{user.profile.file.name}',
            HTTP_HOST='localhost',
        )

        assert response.status_code == 200
        assert b''.join(response.streaming_content) == b'GIF89a'
        assert Path(user.profile.file.path).is_file()


@pytest.mark.django_db
def test_missing_profile_file_is_returned_as_null(
    api_client,
    create_customer,
    tmp_path,
):
    with override_settings(MEDIA_ROOT=tmp_path):
        user = create_customer('missing_media', 'password')
        user.profile.file.name = 'profiles/missing.jpg'
        user.profile.save(update_fields=['file'])
        api_client.force_authenticate(user=user)

        response = api_client.get(f'/api/profile/{user.profile.pk}/')

        assert response.status_code == 200
        assert response.data['file'] is None
