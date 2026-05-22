"""Models for offers and offer packages (Offer, OfferDetail).

Contains the primary models for services offered and their package details.
"""
from django.contrib.auth.models import User
from django.db import models


class Offer(models.Model):
    """Represents a service offer created by a user.

    Fields
    - user: Reference to the creating user.
    - title: Offer title.
    - image: Optional preview image.
    - description: Detailed description of the offer.
    - created_at: Creation timestamp (auto_now_add).
    - updated_at: Last modification timestamp (auto_now).
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='offers',
        verbose_name='Creator'
    )
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='offers/', null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'Offer'
        verbose_name_plural = 'Offers'

    def __str__(self):
        return f"{self.title} by {self.user.username}"


class OfferDetail(models.Model):
    """Package detail for an `Offer` including price and feature information.

    Fields
    - offer: ForeignKey to the related `Offer`.
    - title: Package title.
    - revisions: Number of allowed revisions (-1 for unlimited).
    - delivery_time_in_days: Delivery time in days.
    - price: Package price as a decimal.
    - features: JSON list of feature descriptions.
    - offer_type: Choice between Basic/Standard/Premium.
    """
    class OfferType(models.TextChoices):
        BASIC = 'basic', 'Basic'
        STANDARD = 'standard', 'Standard'
        PREMIUM = 'premium', 'Premium'

    offer = models.ForeignKey(
        Offer,
        on_delete=models.CASCADE,
        related_name='details'
    )
    title = models.CharField(max_length=200)
    revisions = models.IntegerField(default=-1)
    delivery_time_in_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=list)
    offer_type = models.CharField(max_length=20, choices=OfferType.choices)

    class Meta:
        ordering = ['price']
        verbose_name = 'Offer Detail'
        verbose_name_plural = 'Offer Details'
        unique_together = ['offer', 'offer_type']

    def __str__(self):
        return f"{self.offer.title} - {self.offer_type}"
