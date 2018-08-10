from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserWithDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email','first_name','last_name')
