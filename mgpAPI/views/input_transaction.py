from mgpAPI.views.erp_mixin import ErpSyncedApiMixedIn
from transactions.models import InputDetail, Transaction
from mgpAPI.serializers.input_transaction_serializers import TransactionSerializer, InputCostSerializer, \
    InputQuantitySerializer, ReportInput
from products.models import Product
from mgpAPI.erp_services.syn_all import syncall
from rest_framework import generics, response
from mgpAPI.pages.page import StandardResultsSetPagination
from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models import Sum


class InputTransactionList(ErpSyncedApiMixedIn, generics.ListCreateAPIView):
    pagination_class = StandardResultsSetPagination
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """

        return Transaction.objects.filter(types=0)


class InputTransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class InputReportCost(viewsets.ViewSet):
    # Required for the Browsable API renderer to have a nice form.

    serializer_class = InputCostSerializer

    def list(self, request):
        syncall()

        # product_all = Product.objects.all().annotate(sum_amt=Sum('inputdetail__amount'))

        def amount_input_transaction(product_all):
            for product in product_all:
                yield ReportInput(
                    group="Transaction Input Product Cost",
                    keys="TLC" + str(product.id),
                    nameEn=product.title,

                )

        serializer = InputCostSerializer(instance=amount_input_transaction(Product.objects.all()), many=True)
        return Response(serializer.data)


class InputReportQuantity(viewsets.ViewSet):
    # Required for the Browsable API renderer to have a nice form.

    serializer_class = InputQuantitySerializer

    def list(self, request):
        syncall()

        # product_all = Product.objects.all().annotate(sum_qty=Sum('inputdetail__quantity'))

        def data_input_transaction(product_all):
            for product in product_all:
                yield ReportInput(
                    group="Transaction Input Product Quantity",
                    keys="TLQ" + str(product.id),
                    nameEn=product.title,

                )

        serializer = InputQuantitySerializer(instance=data_input_transaction(Product.objects.all()), many=True)
        return Response(serializer.data)
