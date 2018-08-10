from common.master_models import Sector
from mgpAPI.serializers.shift_serializers import ShiftSerializer
from rest_framework import generics
from mgpAPI.pages.page import StandardResultsSetPagination
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from collections import OrderedDict
from rest_framework.response import Response
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
            ('total', Sector.objects.count()),
            ('results', data)
        ]))


class ShiftList(generics.ListCreateAPIView):
    pagination_class = Select2Pagination
    queryset = Sector.objects.all()
    serializer_class = ShiftSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        return Sector.objects.filter(soft_delete=False)

    filter_backends = (DjangoFilterBackend, SearchFilter,OrderingFilter)
    ordering_fields = ('title')
    search_fields = ('title')


class ShiftDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sector.objects.all()
    serializer_class = ShiftSerializer
