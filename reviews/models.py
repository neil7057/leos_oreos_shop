from django.db import models
from django.core.validators import (
    MaxValueValidator, MinValueValidator
)
from django.contrib.auth.models import User
from products.models import Product


class Review(models.Model):
    """ Review Model """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name="reviews",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviews"
    )
    created_on = models.DateField(
        auto_now_add=True,
        blank=False,
        null=False
    )
    title = models.CharField(
        max_length=40,
        blank=False,
        null=False
    )
    content = models.TextField(
        max_length=500
    )
    rating = models.DecimalField(
        max_digits=3, decimal_places=2, null=False,
        validators=[
            MaxValueValidator
            (5, message="Glad you're so pleased but Maximum score is 5!"),
            MinValueValidator
            (1, message="Score must be 1 or more - Be Generous!")
        ],
        blank=False, default=0)

    is_approved = models.BooleanField(
        default=True
    )

    def __str__(self):
        """ String representation of Review title """
        return self.title
