from units.models import Unit
from products.models import Product
from mgpAPI.serializers.unit_serializers import UnitWithUnitCategoryTitleSerializer, UnitSerializer
from rest_framework import generics
from mgpAPI.pages.page import StandardResultsSetPagination
from mgpAPI.views.erp_mixin import ErpSyncedApiMixedIn
from rest_framework import serializers
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from collections import OrderedDict
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination

class Select2Pagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'page'
    page_size_query_param = 'limit'

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('total', Unit.objects.count()),
            ('results', data)
        ]))

class UnitList(ErpSyncedApiMixedIn,generics.ListCreateAPIView):
    pagination_class = Select2Pagination
    queryset = Unit.objects.all()
    serializer_class = UnitWithUnitCategoryTitleSerializer

    def get_serializer_class(self):

        if self.request.method == 'GET':
            serializer_class = UnitWithUnitCategoryTitleSerializer
        else:
            serializer_class = UnitSerializer
        return serializer_class

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        if self.request.GET.get("q"):
            return Unit.objects.filter(unit_category__id=self.request.GET.get("q"),soft_delete=False)
        return Unit.objects.filter(soft_delete=False)

    filter_backends = (DjangoFilterBackend,SearchFilter,OrderingFilter)
    ordering_fields = ('ext_code', 'title','unit_category__title')
    search_fields = ('title', 'ext_code')


class UnitDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer

class UnitFilterByProduct(generics.ListAPIView):
    pagination_class = StandardResultsSetPagination
    queryset = Unit.objects.all()
    serializer_class = UnitWithUnitCategoryTitleSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        if self.request.GET.get("q"):
            try:
                product_instance = Product.objects.get(id=self.request.GET.get("q"))
            except Exception as e:
                raise serializers.ValidationError({"error": "this product pk not found"})
            unit_isntance = product_instance.uom
            unit_category_intance = unit_isntance.unit_category
            return Unit.objects.filter(unit_category=unit_category_intance,soft_delete=False)
        return Unit.objects.filter(soft_delete=False)