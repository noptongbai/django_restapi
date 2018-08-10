from units.models import Unit
from rest_framework.serializers import ModelSerializer
from  mgpAPI.serializers.unit_category_serializers import UnitCategoryOnlyTitleSerializer


class UnitWithTitleSerializer(ModelSerializer):

    class Meta:
        model = Unit
        fields = ('id','title')

class UnitWithUnitCategoryTitleSerializer(ModelSerializer):
    unit_category = UnitCategoryOnlyTitleSerializer()

    class Meta:
        model = Unit
        fields = '__all__'


class UnitSerializer(ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        validated_data["last_modified_users"] = self.context['request'].user
        validated_data["created_user"] = self.context['request'].user

        unit = Unit.objects.create(**validated_data)

        return unit

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.unit_category = validated_data.get('unit_category', instance.unit_category)
        instance.title = validated_data.get('title', instance.title)
        instance.ext_code = validated_data.get('ext_code', instance.ext_code)
        instance.type = validated_data.get('type', instance.type)
        instance.description = validated_data.get('description', instance.description)
        instance.ratio = validated_data.get('ratio', instance.ratio)
        instance.last_modified_users = self.context['request'].user
        instance.soft_delete = validated_data.get('soft_delete', instance.soft_delete)
        instance.save()
        return instance
