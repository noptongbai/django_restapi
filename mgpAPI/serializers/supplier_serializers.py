from common.master_models import Supplier
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers


class SupplierSerializer(ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        validated_data["last_modified_users"] = self.context['request'].user
        validated_data["created_user"] = self.context['request'].user

        return Supplier.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.ext_code = validated_data.get('ext_code', instance.ext_code)
        instance.description = validated_data.get('description', instance.description)
        instance.last_modified_users = self.context['request'].user
        instance.soft_delete = validated_data.get('soft_delete', instance.soft_delete)
        instance.save()
        return instance
