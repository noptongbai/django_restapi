from mgpAPI.views.erp_mixin import ErpSyncedApiMixedIn
from mgpAPI.serializers.manufacturing_allhead_serializers import ConsumptionAllHeadSerializer,ManufacturingTransactionSerializer
from conclusion.models import Consumtion,ManufacturingTransaction
from rest_framework import generics, response
from mgpAPI.pages.page import StandardResultsSetPagination


class FuelHeadConsumptionList(ErpSyncedApiMixedIn, generics.ListCreateAPIView):
    pagination_class = StandardResultsSetPagination
    queryset = Consumtion.objects.all()
    serializer_class = ConsumptionAllHeadSerializer

class MonitorConsumptionList(ErpSyncedApiMixedIn, generics.ListCreateAPIView):
    pagination_class = StandardResultsSetPagination
    queryset = ManufacturingTransaction.objects.all()
    serializer_class = ManufacturingTransactionSerializer