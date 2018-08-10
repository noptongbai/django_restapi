from mgpAPI.views.erp_mixin import ErpSyncedApiMixedIn
from mgpAPI.serializers.manufacturing_generation_serializers import ConsumptionGenerationSerializer
from mgpAPI.serializers.manufacturing_shifthead_serializers import ReportPowerExportSerializer, \
    ReportPowerGenerationSerializer, ReportPowerSteamSerializer,PowerGenerationSerializer
from conclusion.models import Consumtion, PowerGeneration
from rest_framework import generics, response
from mgpAPI.pages.page import StandardResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status

class ShiftHeadConsumptionList(ErpSyncedApiMixedIn, generics.ListCreateAPIView):
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        # return check_permission_product_group(self)
        if self.kwargs.get('date') != None:
            array_date = []
            for x in self.kwargs['date'].split('-'):
                array_date.append(x)
            return Consumtion.objects.filter(created_date__year=array_date[0], created_date__day=array_date[1],
                                         created_date__month=array_date[2])
        return Consumtion.objects.all()

    serializer_class = ConsumptionGenerationSerializer


class ReportPowerGeneration(ErpSyncedApiMixedIn, generics.ListCreateAPIView):
    queryset = PowerGeneration.objects.all()
    serializer_class = ReportPowerGenerationSerializer

class ReportPowerGenerationLast(ErpSyncedApiMixedIn, generics.ListCreateAPIView):
    queryset = PowerGeneration.objects.all()
    serializer_class = ReportPowerGenerationSerializer

class ReportPowerExport(ErpSyncedApiMixedIn, generics.ListCreateAPIView):
    queryset = PowerGeneration.objects.all()
    serializer_class = ReportPowerExportSerializer


class ReportPowerSteam(ErpSyncedApiMixedIn, generics.ListCreateAPIView):
    queryset = PowerGeneration.objects.all()
    serializer_class = ReportPowerSteamSerializer

class PowerGenerationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PowerGeneration.objects.all()
    serializer_class = PowerGenerationSerializer

    def retrieve(self, request, *args, **kwargs):
        print "yes"
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)