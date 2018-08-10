from mgpAPI.views.erp_mixin import ErpSyncedApiMixedIn
from transactions.models import Transaction
from mgpAPI.serializers.adjust_transaction_serializers import TransactionSerializer
from rest_framework import generics, response
from mgpAPI.pages.page import StandardResultsSetPagination


class AdjustTransactionList(ErpSyncedApiMixedIn, generics.ListCreateAPIView):
    pagination_class = StandardResultsSetPagination
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        return Transaction.objects.filter(types=4)


class AdjustTransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
