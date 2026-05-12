from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    class Status(models.TextChoices):
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    customer_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_orders', verbose_name='Customer')
    business_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='business_orders', verbose_name='Business')
    title = models.CharField(max_length=200)
    revisions = models.IntegerField(default=0)
    delivery_time_in_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=list)
    offer_type = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.IN_PROGRESS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f"Order {self.id}: {self.title} ({self.status})"
