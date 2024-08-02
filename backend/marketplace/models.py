from django.db import models
from django.contrib.auth.models import User

class Products(models.Model):
    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('fashion', 'Fashion'),
        ('home', 'Home'),
        ('beauty', 'Beauty'),
        ('sports', 'Sports'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    seller_profile_name = models.CharField(max_length=255)
    seller_profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    views = models.PositiveIntegerField(default=0)  
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)  
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)