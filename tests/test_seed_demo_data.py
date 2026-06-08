from django.core.management import call_command
from django.test import override_settings
import pytest

from offers_app.models import Offer, OfferDetail
from orders_app.models import Order
from profile_app.models import Profile
from reviews_app.models import Review


@pytest.mark.django_db
def test_seed_demo_data_is_complete_and_idempotent(tmp_path):
    with override_settings(MEDIA_ROOT=tmp_path):
        call_command("seed_demo_data")
        first_counts = (
            Profile.objects.count(),
            Offer.objects.count(),
            OfferDetail.objects.count(),
            Review.objects.count(),
            Order.objects.count(),
        )
        call_command("seed_demo_data")
        second_counts = (
            Profile.objects.count(),
            Offer.objects.count(),
            OfferDetail.objects.count(),
            Review.objects.count(),
            Order.objects.count(),
        )

    assert first_counts == (7, 12, 36, 8, 6)
    assert second_counts == first_counts
    assert all(profile.file for profile in Profile.objects.all())
    assert all(offer.image for offer in Offer.objects.all())
