from rest_framework import generics
from  rest_framework import serializers
from mgpAPI.erp_services.syn_all import syncall
from rest_framework.response import Response
from rest_framework import viewsets
from mgpAPI.serializers.all_report import ReportAll, ReportAllSerializer
from mgpAPI.report_config.filter_all import filter_all
from mgpAPI.report_config.keys import create_data


class TaskViewSet(viewsets.ViewSet):
    # Required for the Browsable API renderer to have a nice form.
    serializer_class = ReportAllSerializer

    def list(self, request):
        syncall()
        filter_params = request.GET
        array_period = filter_all(filter_params)
        array_data = create_data(filter_params)

        report_all = {
            1: ReportAll(
                categories=array_period
                ,
                series=array_data
            ),

        }

        serializer = ReportAllSerializer(instance=report_all.values(), many=True)
        return Response(serializer.data)
