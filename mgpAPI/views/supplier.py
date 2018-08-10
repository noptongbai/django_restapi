from common.master_models import Supplier
from mgpAPI.serializers.supplier_serializers import SupplierSerializer
from rest_framework import generics
from mgpAPI.pages.page import StandardResultsSetPagination
from mgpAPI.views.erp_mixin import ErpSyncedApiMixedIn
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination


class Select2Pagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'page'
    page_size_query_param = 'limit'


    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('total', Supplier.objects.count()),
            ('results', data)
        ]))


class SupplierList(ErpSyncedApiMixedIn, generics.ListCreateAPIView):
    pagination_class = Select2Pagination
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        return Supplier.objects.filter(soft_delete=False)

    filter_backends = (DjangoFilterBackend, SearchFilter,OrderingFilter)
    ordering_fields = ('ext_code', 'title')
    search_fields = ('title','ext_code')


class SupplierDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
