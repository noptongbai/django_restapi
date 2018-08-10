from units.models import UnitCategory
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers


class UnitCategoryOnlyTitleSerializer(ModelSerializer):
    class Meta:
        model = UnitCategory
        fields = ('id', 'title')


class UnitCategorySerializer(ModelSerializer):
    unit_count = serializers.IntegerField(
        source='unit_set.count',
        read_only=True
    )

    class Meta:
        model = UnitCategory
        fields = ('id', 'title','description','soft_delete','unit_count')

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        validated_data["last_modified_users"] = self.context['request'].user
        validated_data["created_user"] = self.context['request'].user

        return UnitCategory.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.last_modified_users = self.context['request'].user
        instance.soft_delete = validated_data.get('soft_delete', instance.soft_delete)
        instance.save()
        return instance
