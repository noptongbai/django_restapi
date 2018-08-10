from rest_framework import generics
from  rest_framework import serializers
from mgpAPI.erp_services.syn_all import syncall
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.db import transaction
from conclusion.models import PowerGeneration
from rest_framework import serializers
from common.master_models import Sector


class PowerExtendViews(viewsets.ViewSet):
    # Required for the Browsable API renderer to have a nice form.

    def list(self, request):
        return Response()

    @transaction.atomic
    def post(self, request, format=None):
        if request.data.get("power") == None:
            raise serializers.ValidationError({"error": "need power"})
        for power in request.data["power"]:

            try:
                p = PowerGeneration.objects.get(id=power["id"])
            except Exception:
                raise serializers.ValidationError({"error": "not pk generations found " + '%d' % power["id"]})

            try:
                sector = Sector.objects.get(id=power["sector"])
            except Exception:
                raise serializers.ValidationError({"error": "not pk Sector found " + '%d' % power["sector"]})

            try:
                if power.get("sector") != None:
                    p.sector = sector
                if power.get("generate_meter") != None:
                    p.generate_meter = power.get("generate_meter")
                if power.get("mdb_meter") != None:
                    p.mdb_meter = power.get("mdb_meter")
                if power.get("export_meter") != None:
                    p.export_meter = power.get("export_meter")
                if power.get("steam") != None:
                    p.steam = power.get("steam")
                if power.get("weight_scale_meter") != None:
                    p.weight_scale_meter = power.get("weight_scale_meter")
                p.last_modified_users = request.user
                p.save()
            except Exception:
                raise serializers.ValidationError({"error": "data mis match"})

        return Response(status=status.HTTP_200_OK)
