from mgpAPI.views.erp_mixin import ErpSyncedApiMixedIn
from products.models import ProductCategory
from mgpAPI.serializers.product_category_serializers import ProductCategorySerializer
from rest_framework import generics
from mgpAPI.pages.page import StandardResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from collections import OrderedDict
from rest_framework.response import Response
from  mgpAPI.permissions.group_permissions import HasGroupPermission
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
            ('total', ProductCategory.objects.count()),
            ('results', data)
        ]))


class ProductCategoryList(ErpSyncedApiMixedIn, generics.ListCreateAPIView):
    pagination_class = Select2Pagination
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer

    # permission_classes = [HasGroupPermission]
    # required_groups = {
    #     'GET' : ['moderators'],
    #     'POST': ['moderators'],
    # }
    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        return ProductCategory.objects.filter(soft_delete=False)

    filter_backends = (DjangoFilterBackend, SearchFilter,OrderingFilter)
    ordering_fields = ('ext_code', 'title')
    search_fields = ('title', 'ext_code')


class ProductCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
