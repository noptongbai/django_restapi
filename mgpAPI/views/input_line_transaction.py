from mgpAPI.views.erp_mixin import ErpSyncedApiMixedIn
from transactions.models import InputDetail
from rest_framework import serializers
from products.models import Product
from mgpAPI.serializers.input_transaction_serializers import  InputDetailSerializer
from rest_framework import generics, response
from mgpAPI.pages.page import StandardResultsSetPagination


class InputLineTransactionList(ErpSyncedApiMixedIn,generics.ListAPIView):
    pagination_class = StandardResultsSetPagination
    queryset = InputDetail.objects.all()
    serializer_class = InputDetailSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        if self.request.GET.get("q"):
            try:
                product_instance = Product.objects.get(id=self.request.GET.get("q"))
            except Exception as e:
                raise serializers.ValidationError({"error": "this product pk not found"})

            return InputDetail.objects.filter(left_quantity__gt=0,product=product_instance)
        return InputDetail.objects.filter(left_quantity__gt=0)



