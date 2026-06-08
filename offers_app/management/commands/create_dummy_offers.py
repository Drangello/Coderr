# -*- coding: utf-8 -*-
"""Management command to generate dummy offers for testing.
Creates 4 users (if not existent) and 3 offers per user, each with
basic, standard and premium OfferDetail entries. Uses a local placeholder
image stored in MEDIA_ROOT/offers/placeholder_offer.png.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from offers_app.models import Offer, OfferDetail
from django.core.files import File
import os

class Command(BaseCommand):
    help = 'Generate dummy offers (4 users, 3 offers each)'

    def handle(self, *args, **options):
        User = get_user_model()
        usernames = ['alice', 'bob', 'carol', 'dave']
        placeholder_path = os.path.join('media', 'offers', 'placeholder_offer.png')
        if not os.path.isfile(placeholder_path):
            self.stdout.write(self.style.WARNING('Placeholder image not found: {}'.format(placeholder_path)))
        for username in usernames:
            user, created = User.objects.get_or_create(username=username, defaults={'password': 'test1234'})
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created user {username}'))
            for i in range(1, 4):
                offer = Offer.objects.create(
                    user=user,
                    title=f'Demo‑Angebot {i} von {username}',
                    description='Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
                    image=File(open(placeholder_path, 'rb')) if os.path.isfile(placeholder_path) else None,
                )
                for kind, price in [('basic', 99), ('standard', 199), ('premium', 299)]:
                    OfferDetail.objects.create(
                        offer=offer,
                        title=f'{kind.title()} Paket',
                        revisions=-1,
                        delivery_time_in_days=5,
                        price=price,
                        features=['Feature A', 'Feature B', 'Feature C'],
                        offer_type=kind,
                    )
        self.stdout.write(self.style.SUCCESS('Dummy offers successfully created.'))
