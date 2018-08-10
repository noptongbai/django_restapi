from mgpAPI.serializers.transaction_seializers import TransactionSerializer
from mgpAPI.views.erp_mixin import ErpSyncedApiMixedIn
from transactions.models import Transaction
from rest_framework import generics
from mgpAPI.pages.page import StandardResultsSetPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from collections import OrderedDict
from rest_framework.response import Response
from datetime import datetime


class Select2Pagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'page'
    page_size_query_param = 'limit'

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('total', Transaction.objects.count()),
            ('results', data)
        ]))


class TransactionList(ErpSyncedApiMixedIn, generics.ListAPIView):
    pagination_class = Select2Pagination
    queryset = Transaction.objects.all()

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

            return Transaction.objects.filter(created_date__range=(start_datetime, end_datetime))
        return Transaction.objects.all()

    serializer_class = TransactionSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    search_fields = ('types')
