from django.db import models
from django.contrib.auth.models import User

# Create your models here.  
class Products(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products',null=True)
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
