"""Models for orders (Order).

Contains the `Order` model representing orders between customers and businesses.
"""
from django.contrib.auth.models import User
from django.db import models


class Order(models.Model):
    """Represents an order placed by a customer for a business offering.

    Fields
    - customer_user: The customer who placed the order.
    - business_user: The business fulfilling the order.
    - title: Short title of the order.
    - revisions: Number of allowed revisions.
    - delivery_time_in_days: Delivery time in days.
    - price: Price of the order.
    - features: JSON list of additional features.
    - offer_type: Type of the ordered offer.
    - status: Order status (in_progress/completed/cancelled).
    - created_at/updated_at: Timestamps.
    """
    class Status(models.TextChoices):
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    customer_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='customer_orders',
        verbose_name='Customer'
    )
    business_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='business_orders',
        verbose_name='Business'
    )
    title = models.CharField(max_length=200)
    revisions = models.IntegerField(default=0)
    delivery_time_in_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=list)
    offer_type = models.CharField(max_length=50)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.IN_PROGRESS
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f"Order {self.id}: {self.title} ({self.status})"
