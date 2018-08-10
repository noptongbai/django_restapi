from mgpAPI.views.erp_mixin import ErpSyncedApiMixedIn
from mgpAPI.serializers.manufacturing_outage_serializers import ConsumptionOutageSerializer
from mgpAPI.serializers.manufacturing_shifthead_serializers import ReportOutagePlannedSerializer, \
    ReportOutageSerializer, ReportOutageUnplannedSerializer, ReportOutageVariabilitySerializer,OutageSerializer
from conclusion.models import Consumtion, Outage
from rest_framework import generics, response
from mgpAPI.pages.page import StandardResultsSetPagination



class OutageConsumptionList(ErpSyncedApiMixedIn, generics.ListCreateAPIView):
    pagination_class = StandardResultsSetPagination
    queryset = Consumtion.objects.all()
    serializer_class = ConsumptionOutageSerializer


class ReportOutageConsumptionList(ErpSyncedApiMixedIn, generics.ListCreateAPIView):
    queryset = Outage.objects.all()
    serializer_class = ReportOutageSerializer


class ReportOutageVariabilityConsumptionList(ErpSyncedApiMixedIn, generics.ListCreateAPIView):
    queryset = Outage.objects.filter(planned_outage=2)
    serializer_class = ReportOutageVariabilitySerializer


class ReportOutagePlannedConsumptionList(ErpSyncedApiMixedIn, generics.ListCreateAPIView):
    queryset = Outage.objects.filter(planned_outage=0)
    serializer_class = ReportOutagePlannedSerializer


class ReportOutageUnplannedConsumptionList(ErpSyncedApiMixedIn, generics.ListCreateAPIView):
    queryset = Outage.objects.filter(planned_outage=1)
    serializer_class = ReportOutageUnplannedSerializer

class OutageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Outage.objects.all()
    serializer_class = OutageSerializer
