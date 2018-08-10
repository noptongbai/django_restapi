from mgpAPI.erp_services.syn_all import syncall
from rest_framework.response import Response
from rest_framework import viewsets
from mgpAPI.serializers.daily_report import ReportDailyDateSerializer
from mgpAPI.daily_report_config.month_report import add_data_month
from mgpAPI.daily_report_config.daily_report import add_data_daily
from mgpAPI.daily_report_config.export_csv import create_file_date, create_file_month
from django.http import HttpResponse
import json


class DailyReport(viewsets.ViewSet):
    # Required for the Browsable API renderer to have a nice form.
    serializer_class = ReportDailyDateSerializer

    def list(self, request):
        syncall()
        filter_params = request.GET
        if filter_params.get("export_csv") == "true":
            if filter_params.get("date") != None:
                array_data = add_data_daily(filter_params["date"])
                path = create_file_date(array_data)
                response_data = {}
                response_data['success'] = True
                response_data['name'] = path
                return HttpResponse(json.dumps(response_data), content_type="application/json")

            else:

                array_data = add_data_month(filter_params["month"])
                path = create_file_month(array_data)
                response_data = {}
                response_data['success'] = True
                response_data['name'] = path
                return HttpResponse(json.dumps(response_data), content_type="application/json")


        else:
            if filter_params.get("date") != None:
                array_data = add_data_daily(filter_params["date"])
                serializer = ReportDailyDateSerializer(instance=array_data.values(), many=True)
                return Response(serializer.data)

            else:
                array_data = add_data_month(filter_params["month"])

                serializer = ReportDailyDateSerializer(instance=array_data.values(), many=True)
                return Response(serializer.data)
