from transactions.models import Transaction
from rest_framework.serializers import ModelSerializer
from mgpAPI.serializers.user_serializers import UserWithDetailSerializer


class TransactionSerializer(ModelSerializer):
    created_user = UserWithDetailSerializer()
    last_modified_users = UserWithDetailSerializer()

    class Meta:
        model = Transaction
        fields = '__all__'
