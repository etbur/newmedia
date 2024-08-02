from rest_framework import serializers
from .models import Products
from rest_framework import serializers
from .models import Products

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = [
            'id', 'name', 'price', 'description', 'image', 
            'seller_profile_name', 'seller_profile_picture', 
            'category', 'views', 'rating', 'created_at', 'updated_at'
        ]
