from rest_framework import generics
from mgpAPI.pages.page import StandardResultsSetPagination
from mgpAPI.serializers.product_serializers import ProductSerializer, ProductWithCategoryTitleSerializer, \
    ProductReportQuantitySerializer, ProductReportCostSerializer
from mgpAPI.views.erp_mixin import ErpSyncedApiMixedIn
from products.models import Product
from mgpAPI.permissions.model_permission import BaseModelPerm
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from collections import OrderedDict
from rest_framework.response import Response
from  mgpAPI.permissions.group_permissions import HasGroupPermission
from  mgpAPI.permissions.group_product_permissions import check_permission_product_group


class Select2Pagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'page'
    page_size_query_param = 'limit'

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('total', Product.objects.count()),
            ('results', data)
        ]))


class StandardResultsSetPagination(LimitOffsetPagination, PageNumberPagination):
    default_limit = 10
    limit_query_param = 'iDisplayLength'
    offset_query_param = 'iDisplayStart'
    page_query_param = 'page'
    max_limit = 100

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('recordsTotal', self.count),
            ('recordsFiltered', self.count),
            ('data', data)
        ]))


class ProductList(ErpSyncedApiMixedIn, generics.ListCreateAPIView):
    pagination_class = Select2Pagination
    queryset = Product.objects.all()
    serializer_class = ProductWithCategoryTitleSerializer

    def get_serializer_class(self):

        if self.request.method == 'GET':
            serializer_class = ProductWithCategoryTitleSerializer
        else:
            serializer_class = ProductSerializer
        return serializer_class
    
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    ordering_fields = ('title', 'title2', 'ext_code', 'product_category__title', 'uom__title', 'quantity')
    search_fields = ('title', 'uom__title')
    filter_fields = ('title', 'uom__title')


class ProductListReportQuantity(ErpSyncedApiMixedIn, generics.ListCreateAPIView):
    queryset = Product.objects.all().only('id', 'title')
    serializer_class = ProductReportQuantitySerializer
    # permission_classes = [IsOwnerOrReadOnly, BaseModelPerm]
    # model_permissions = Product

    # def get_queryset(self):
    #     if self.request.GET.get("q"):
    #         return Product.objects.filter(product_category__id=self.request.GET.get("q"), soft_delete=False)


class ProductListReportCost(ErpSyncedApiMixedIn, generics.ListCreateAPIView):
    queryset = Product.objects.all().only('id', 'title')
    serializer_class = ProductReportCostSerializer
    # permission_classes = [IsOwnerOrReadOnly, BaseModelPerm]
    # model_permissions = Product

    # def get_queryset(self):
    #     if self.request.GET.get("q"):
    #         return Product.objects.filter(product_category__id=self.request.GET.get("q"), soft_delete=False)


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [IsOwnerOrReadOnly]
