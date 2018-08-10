from mgpAPI.views.erp_mixin import ErpSyncedApiMixedIn
from mgpAPI.erp_services.syn_all import syncall
from transactions.models import Transaction, WithdrawDetail
from mgpAPI.serializers.withdraw_transaction_serailizers import TransactionSerializer, WithdrawCostSerializer, \
    WithdrawQuantitySerializer, ReportWithdraw
from rest_framework import generics, response
from mgpAPI.pages.page import StandardResultsSetPagination
from rest_framework import viewsets
from rest_framework.response import Response
from product import Product
from django.db.models import Sum


class WithdrawTransactionList(ErpSyncedApiMixedIn, generics.ListCreateAPIView):
    pagination_class = StandardResultsSetPagination
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        return Transaction.objects.filter(types=1)


class WithdrawTransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class WithdrawReportCost(viewsets.ViewSet):
    # Required for the Browsable API renderer to have a nice form.

    serializer_class = WithdrawCostSerializer

    def list(self, request):
        syncall()

        # product_all = Product.objects.all().annotate(sum_amt=Sum('withdrawdetail__amount'))

        def amount_input_transaction(product_all):
            for product in product_all:
                yield ReportWithdraw(
                    group="Transaction Withdraw Product Cost",
                    keys="TWC" + str(product.id),
                    nameEn=product.title,

                )

        serializer = WithdrawCostSerializer(instance=amount_input_transaction(Product.objects.all()), many=True)
        return Response(serializer.data)


class WithdrawReportQuantity(viewsets.ViewSet):
    # Required for the Browsable API renderer to have a nice form.

    serializer_class = WithdrawQuantitySerializer

    def list(self, request):
        syncall()

        # product_all = Product.objects.all().annotate(sum_qty=Sum('withdrawdetail__quantity'))

        def data_input_transaction(product_all):
            for product in product_all:
                yield ReportWithdraw(
                    group="Transaction Withdraw Product Quantity",
                    keys="TWQ" + str(product.id),
                    nameEn=product.title,

                )

        serializer = WithdrawQuantitySerializer(instance=data_input_transaction(Product.objects.all()), many=True)
        return Response(serializer.data)
