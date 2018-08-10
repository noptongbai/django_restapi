from mgpAPI.views.erp_mixin import ErpSyncedApiMixedIn
from rest_framework import generics, response
from mgpAPI.pages.page import StandardResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from conclusion.models import ManufacturingTransaction, ManufacturingTransactionLine, Outage, PowerGeneration, \
    Consumtion
from  mgpAPI.serializers.manufacturing_shifthead_serializers import ManufacturingTransactionSerializer, \
    OutageSerializer, PowerGenerationSerializer, PowerGenerationSerializerLast
from datetime import datetime
from django.db.models import Q
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from collections import OrderedDict
from rest_framework.response import Response


class Select2PaginationPower(PageNumberPagination):
    page_size = 1000
    page_query_param = 'page'
    page_size_query_param = 'limit'

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('total', PowerGeneration.objects.count()),
            ('results', data)
        ]))


class Select2PaginationOutage(PageNumberPagination):
    page_size = 5
    page_query_param = 'page'
    page_size_query_param = 'limit'

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('total', Outage.objects.count()),
            ('results', data)
        ]))


class Select2PaginationConsumtion(PageNumberPagination):
    page_size = 5
    page_query_param = 'page'
    page_size_query_param = 'limit'

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('total', ManufacturingTransaction.objects.count()),
            ('results', data)
        ]))


class GenerationConsumptionMonitor(ErpSyncedApiMixedIn, generics.ListCreateAPIView):
    pagination_class = Select2PaginationPower

    def get_queryset(self):
        # return check_permission_product_group(self)

        if self.request.query_params.get('date') != None:
            array_date = []

            for x in self.request.query_params['date'].split('-'):
                array_date.append(x)

            return PowerGeneration.objects.filter(created_date__year=array_date[0], created_date__month=array_date[1],
                                                  created_date__day=array_date[2])
        return PowerGeneration.objects.all()

    serializer_class = PowerGenerationSerializer


class GenerationConsumptionMonitorLast(ErpSyncedApiMixedIn, generics.ListCreateAPIView):
    def get_queryset(self):
        # return check_permission_product_group
        id = PowerGeneration.objects.order_by('-created_date','-hours')[0].id
        return PowerGeneration.objects.filter(id=id)

    serializer_class = PowerGenerationSerializerLast


class ConsumptionMonitor(ErpSyncedApiMixedIn, generics.ListCreateAPIView):
    pagination_class = Select2PaginationConsumtion

    def get_queryset(self):
        # return check_permission_product_group(self)
        if self.request.query_params.get('start_date') != None and self.request.query_params.get('end_date') != None:

            start_date = []
            end_date = []

            for x in self.request.query_params['start_date'].split('-'):
                start_date.append(int(x))

            start_datetime = datetime(
                year=start_date[0],
                month=start_date[1],
                day=start_date[2]
            )

            for x in self.request.query_params['end_date'].split('-'):
                end_date.append(int(x))

            end_datetime = datetime(
                year=end_date[0],
                month=end_date[1],
                day=end_date[2],
                hour=23,
                minute=59,
                second=59
            )

            return ManufacturingTransaction.objects.filter(created_date__range=(start_datetime, end_datetime))
        return ManufacturingTransaction.objects.all()

    serializer_class = ManufacturingTransactionSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id',)


class OutagenMonitor(ErpSyncedApiMixedIn, generics.ListCreateAPIView):
    pagination_class = Select2PaginationOutage

    def get_queryset(self):
        if self.request.query_params.get('start_date') != None and self.request.query_params.get('end_date') != None:

            start_date = []
            end_date = []

            for x in self.request.query_params['start_date'].split('-'):
                start_date.append(int(x))

            start_datetime = datetime(
                year=start_date[0],
                month=start_date[1],
                day=start_date[2]
            )

            for x in self.request.query_params['end_date'].split('-'):
                end_date.append(int(x))

            end_datetime = datetime(
                year=end_date[0],
                month=end_date[1],
                day=end_date[2],
                hour=23,
                minute=59,
                second=59
            )
            return Outage.objects.filter(Q(through_time__range=(start_datetime, end_datetime)) | Q(
                from_time__range=(start_datetime, end_datetime)))
        return Outage.objects.all()

    serializer_class = OutageSerializer
