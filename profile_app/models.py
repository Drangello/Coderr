"""Modelle für Benutzerprofile (Profile).

Enthält das `Profile`-Modell mit zusätzlichen Benutzerdaten.
"""
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """Ergänzende Profildaten für einen `User`.

    Fields
    - user: OneToOne-Verknüpfung zum Django-User.
    - first_name/last_name: Vor- und Nachname (optional).
    - file: Profilbild (optional).
    - location: Standort/Ort.
    - tel: Telefonnummer.
    - description: Freitextbeschreibung.
    - working_hours: Geschäftszeiten (optional).
    - type: Nutzer-Typ (Business oder Customer).
    - created_at: Erstellungszeitpunkt.
    """
    class UserType(models.TextChoices):
        BUSINESS = 'business', 'Business'
        CUSTOMER = 'customer', 'Customer'

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name="User"
    )
    first_name = models.CharField(max_length=150, blank=True, default='')
    last_name = models.CharField(max_length=150, blank=True, default='')
    file = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True,
        verbose_name="Profile Picture"
    )
    location = models.CharField(max_length=200, blank=True, default='')
    tel = models.CharField(max_length=50, blank=True, default='')
    description = models.TextField(blank=True, default='')
    working_hours = models.CharField(max_length=100, blank=True, default='')
    type = models.CharField(
        max_length=20,
        choices=UserType.choices,
        default=UserType.CUSTOMER,
        verbose_name="User Type"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return f"{self.user.username} ({self.type})"
