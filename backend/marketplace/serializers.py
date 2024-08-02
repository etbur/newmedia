from rest_framework import serializers
from .models import Products
from rest_framework import serializers
from .models import Products

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products  # Specify the model
        fields = ['id', 'name', 'price', 'seller_profile_picture', 'seller_profile_name', 'description', 'image', 'category']
