"""Backward-compatible alias for the demo data seed command."""

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Alias for seed_demo_data"

    def handle(self, *args, **options):
        call_command("seed_demo_data")
