from mgpAPI.views.erp_mixin import ErpSyncedApiMixedIn
from mgpAPI.serializers.manufacturing_shifthead_serializers import ConsumptionSerializer
from conclusion.models import Consumtion
from rest_framework import generics, response
from mgpAPI.pages.page import StandardResultsSetPagination


class ShiftHeadConsumptionList(ErpSyncedApiMixedIn, generics.ListCreateAPIView):
    pagination_class = StandardResultsSetPagination
    queryset = Consumtion.objects.all()
    serializer_class = ConsumptionSerializer
