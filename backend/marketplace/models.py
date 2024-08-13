from django.db import models
from django.contrib.auth.models import User
class Products(models.Model):
    CATEGORY_CHOICES = [
        ('electronics', 'electronics'),
        ('fashion', 'fashion'),
        ('home', 'home'),
        ('beauty', 'beauty'),
        ('sports', 'sports'),
        ('other', 'other'),
    ]
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    seller_profile_name = models.CharField(max_length=255)
    seller_profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    views = models.PositiveIntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    location = models.CharField(max_length=255, blank=True, null=True)  # Add location field
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=3, decimal_places=2 ,default=0)

    class Meta:
        unique_together = ('user', 'product')  # Ensure a user can rate a product only once

    def __str__(self):
        return f'{self.user.username} rated {self.product.name} - {self.rating}'
