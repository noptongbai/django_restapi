from common.master_models import Preference
from mgpAPI.serializers.preference_serializers import PreferenceSerializer
from rest_framework import generics
from mgpAPI.pages.page import StandardResultsSetPagination
from mgpAPI.erp_services.syn_all import syncall
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from collections import OrderedDict
from rest_framework.response import Response


class Select2Pagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'page'
    page_size_query_param = 'limit'

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('total', Preference.objects.count()),
            ('results', data)
        ]))


class PreferenceList(generics.ListCreateAPIView):
    pagination_class = Select2Pagination
    queryset = Preference.objects.all()
    serializer_class = PreferenceSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        return Preference.objects.filter(soft_delete=False)


class PreferenceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Preference.objects.all()
    serializer_class = PreferenceSerializer
