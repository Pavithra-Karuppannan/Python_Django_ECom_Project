from rest_framework import serializers
from .models import Products,Category,Cart,Favourite

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Products
        fields='__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cart
        fields='__all__'

class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Favourite
        fields='__all__'