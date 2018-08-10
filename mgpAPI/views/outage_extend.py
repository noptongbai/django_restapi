from rest_framework import generics
from  rest_framework import serializers
from mgpAPI.erp_services.syn_all import syncall
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.db import transaction
from conclusion.models import Outage
from  rest_framework import serializers


class OutageExtendViews(viewsets.ViewSet):
    # Required for the Browsable API renderer to have a nice form.

    def list(self, request):
        return Response()

    @transaction.atomic
    def post(self, request, format=None):

        for outage in request.data["outages"]:
            if request.data.get("outages") == None:
                raise serializers.ValidationError({"error": "need outages"})

            try:
                o = Outage.objects.get(id=outage["id"])
            except Exception:
                raise serializers.ValidationError({"error": "not pk found " + '%d' % outage["id"]})
            if outage.get("delete") == True:
                o.delete()
            else:

                if outage.get("from_time") != None:
                    o.from_time = outage.get("from_time")
                if outage.get("through_time") != None:
                    o.through_time = outage.get("through_time")
                try:
                    if outage.get("planned_outage") != None:
                        o.planned_outage = outage.get("planned_outage")
                    if outage.get("note") != None:
                        o.note = outage.get("note")
                    o.last_modified_users = request.user
                    o.save()
                except Exception:
                    raise serializers.ValidationError({"error": "data mis match"})

        return Response(status=status.HTTP_200_OK)
