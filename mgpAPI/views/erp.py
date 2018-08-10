from rest_framework.views import APIView
from django.http import HttpResponse
from mgpAPI.erp_services.syn_all import syncall
from mgpAPI.erp_services.po_sync import purchase_order_sync, purchase_order_line_sync
from mgpAPI.erp_services.po_rcpt_sync import purchase_order_rcpt_line_sync, purchase_order_rcpt_sync
from mgpAPI.erp_services.jounal_to_erp import transaction_log_sync
from django.db import transaction
from django.utils.decorators import method_decorator
import json


class SyncErpView(APIView):
    """
    API endpoint that allows a device to be viewed.
    """

    @method_decorator(transaction.atomic)
    def get(self, request):
        """
        GET a product_categories
        :rtype: object
        """
        syncall()
        response_data = {}
        response_data['success'] = True
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)


class SyncPoView(APIView):
    """
    API endpoint that allows a device to be viewed.
    """

    @method_decorator(transaction.atomic)
    def get(self, request):
        """
        GET a product_categories
        :rtype: object
        """
        purchase_order_sync()
        purchase_order_line_sync()
        response_data = {}
        response_data['success'] = True
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)


class SyncInputView(APIView):
    """
    API endpoint that allows a device to be viewed.
    """

    @method_decorator(transaction.atomic)
    def get(self, request):
        """
        GET a product_categories
        :rtype: object
        """
        purchase_order_rcpt_sync()
        purchase_order_rcpt_line_sync()
        response_data = {}
        response_data['success'] = True
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)


class SyncToErpInput(APIView):
    def get(self, request):
        """
        GET a product_categories
        :rtype: object
        """
        transaction_log_sync()
        response_data = {}
        response_data['success'] = True
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)
