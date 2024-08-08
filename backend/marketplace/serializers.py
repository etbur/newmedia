from rest_framework import serializers
from .models import Products
from rest_framework import serializers
from .models import Products,Rating

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = [
            'id', 'name', 'price', 'description', 'image', 
            'seller_profile_name', 'seller_profile_picture', 
            'category', 'views', 'created_at', 'updated_at'
        ]

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['user', 'product', 'rating']  # Specify fields to include in the serialized data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.username  # Customize if needed
        representation['product'] = instance.product.id  # Customize if needed
        return representation

