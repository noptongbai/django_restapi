from .models import ProductCategory, Product
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers


class ProductCategorySerializer(ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'


class ProductCategoryOnlyTitleSerializer(ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ('id','title')


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductWithCategoryTitleSerializer(ModelSerializer):
    product_categories = ProductCategoryOnlyTitleSerializer(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
