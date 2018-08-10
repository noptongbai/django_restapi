from products.models import Product
from rest_framework.serializers import ModelSerializer
from  mgpAPI.serializers.product_category_serializers import ProductCategoryOnlyTitleSerializer
from  mgpAPI.serializers.unit_serializers import UnitWithTitleSerializer
from rest_framework import serializers


class ProductWithCategoryTitleSerializer(ModelSerializer):
    product_category = ProductCategoryOnlyTitleSerializer()
    uom = UnitWithTitleSerializer()
    forecast_quantity = serializers.IntegerField(
        source='quantity',
        read_only=True
    )

    class Meta:
        model = Product
        fields = '__all__'


class ProductReportQuantitySerializer(ModelSerializer):
    group = serializers.SerializerMethodField('get_group_product')
    keys = serializers.SerializerMethodField('get_key')
    nameEn = serializers.CharField(source='title')

    def get_key(self, obj):
        return '{}{}'.format('PQ', obj.id)

    def get_group_product(self, obj):
        return "Product Quantity"

    class Meta:
        model = Product
        fields = 'group', 'keys', 'nameEn'


class ProductReportCostSerializer(ModelSerializer):
    group = serializers.SerializerMethodField('get_group_product')
    keys = serializers.SerializerMethodField('get_key')
    nameEn = serializers.CharField(source='title')

    def get_key(self, obj):
        return '{}{}'.format('PC', obj.id)

    def get_group_product(self, obj):
        return "Product Cost"

    class Meta:
        model = Product
        fields = 'group', 'keys', 'nameEn'


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        validated_data["last_modified_users"] = self.context['request'].user
        validated_data["created_user"] = self.context['request'].user

        product = Product.objects.create(**validated_data)

        return product

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.product_category = validated_data.get('product_category', instance.product_category)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.stockable = validated_data.get('stockable', instance.stockable)
        instance.last_modified_users = self.context['request'].user
        instance.soft_delete = validated_data.get('soft_delete', instance.soft_delete)
        instance.save()
        return instance
