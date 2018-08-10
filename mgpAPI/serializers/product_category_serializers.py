from products.models import ProductCategory
from rest_framework.serializers import ModelSerializer
from  rest_framework import  serializers

class ProductCategoryOnlyTitleSerializer(ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ('id', 'title','humidity_type','shift_head_able')


class ProductCategorySerializer(ModelSerializer):
    product_count = serializers.IntegerField(
        source='product_set.count',
        read_only=True
    )

    class Meta:
        model = ProductCategory
        fields = '__all__'

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        validated_data["last_modified_users"] = self.context['request'].user
        validated_data["created_user"] = self.context['request'].user

        return ProductCategory.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.ext_code = validated_data.get('ext_code', instance.ext_code)
        instance.last_modified_users = self.context['request'].user
        instance.humidity_type = validated_data.get('humidity_type', instance.humidity_type)
        instance.description = validated_data.get('description',instance.description)
        instance.shift_head_able = validated_data.get('shift_head_able', instance.shift_head_able)
        instance.soft_delete = validated_data.get('soft_delete', instance.soft_delete)
        instance.save()
        return instance
