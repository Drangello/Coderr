"""Models for reviews (Review).

Contains the `Review` model used to rate business users by reviewers.
"""
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db import models


class Review(models.Model):
    """Represents a review of a business by a reviewer.

    Fields
    - business_user: The business user being reviewed.
    - reviewer: The user who provided the review.
    - rating: Rating value (1-5).
    - description: Free-text review description.
    - created_at/updated_at: Timestamps.
    """
    business_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_reviews',
        verbose_name='Business User'
    )
    reviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='given_reviews',
        verbose_name='Reviewer'
    )
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        unique_together = ['business_user', 'reviewer']

    def __str__(self):
        return (
            f"Review by {self.reviewer.username} "
            f"for {self.business_user.username} ({self.rating}/5)"
        )
