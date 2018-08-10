from common.master_models import Preference
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers


class PreferenceSerializer(ModelSerializer):
    class Meta:
        model = Preference
        fields = '__all__'

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        validated_data["last_modified_users"] = self.context['request'].user
        validated_data["created_user"] = self.context['request'].user

        return Preference.objects.create(**validated_data)

        #raise serializers.ValidationError({'my_field': 'A field error'})

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.key = validated_data.get('key', instance.key)
        instance.value = validated_data.get('value', instance.value)
        instance.description = validated_data.get('description', instance.description)
        instance.last_modified_users = self.context['request'].user
        instance.soft_delete = validated_data.get('soft_delete', instance.soft_delete)
        instance.save()
        return instance
