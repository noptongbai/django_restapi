from mgpAPI.views.erp_mixin import ErpSyncedApiMixedIn
from mgpAPI.serializers.manufacturing_fuelhead_serializers import ConsumptionFuelHeadSerializer
from conclusion.models import Consumtion
from rest_framework import generics, response
from mgpAPI.pages.page import StandardResultsSetPagination


class FuelHeadConsumptionList(ErpSyncedApiMixedIn, generics.ListCreateAPIView):
    pagination_class = StandardResultsSetPagination
    queryset = Consumtion.objects.all()
    serializer_class = ConsumptionFuelHeadSerializer


