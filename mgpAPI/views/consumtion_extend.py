from rest_framework.response import Response
from rest_framework import viewsets, status
from django.db import transaction
from conclusion.models import ManufacturingTransaction, ManufacturingTransactionLine
from rest_framework import serializers
from mgpAPI.services.delete_consumtion import delete_consumtion
from  mgpAPI.erp_services.jounal_to_erp import transaction_log_sync
import sys


class ConsumtionExtendViews(viewsets.ViewSet):
    # Required for the Browsable API renderer to have a nice form.

    def list(self, request):
        return Response()

    @transaction.atomic
    def post(self, request, format=None):

        if request.data.get("delete") == True:
            id = request.data.get("id")
            try:
                manu = ManufacturingTransaction.objects.get(id=id)
                manu_line = ManufacturingTransactionLine.objects.filter(manufacturing_transaction=manu)
                for m in manu_line:
                    delete_consumtion(m.withdraw, request.user, m.product, m.unit, m.quantity)
                    m.delete()
                manu.delete()
                if 'test' not in sys.argv:
                    transaction_log_sync()
                return Response(status=status.HTTP_200_OK)
            except Exception:
                raise serializers.ValidationError({"error": "not pk found " + '%d' % request.data.get("id")})
        else:
            for l in request.data["line"]:
                try:
                    manu_line = ManufacturingTransactionLine.objects.get(id=l["id"])
                    delete_consumtion(manu_line.withdraw, request.user, manu_line.product, manu_line.unit,
                                      manu_line.quantity)
                    manu_line.delete()
                except Exception:
                    raise serializers.ValidationError({"error": "not pk found " + '%d' % l["id"]})

            if 'test' not in sys.argv:
                transaction_log_sync()
            return Response(status=status.HTTP_200_OK)
