from .models import Unit, UnitCategory
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers


class UnitSerializer(ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'


class UnitCategorySerializer(ModelSerializer):
    class Meta:
        model = UnitCategory
        fields = '__all__'


class UnitCategoryOnlyTitleSerializer(ModelSerializer):
    class Meta:
        model = UnitCategory
        fields = ('id', 'title')


class UnitWithCategoryTitleSerializer(ModelSerializer):
    product_categories = UnitCategorySerializer()

    class Meta:
        model = Unit
        fields = '__all__'
