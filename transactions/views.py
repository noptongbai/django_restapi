from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Supplier
from users.models import UserSystem
from rest_framework import status
from django.http import HttpResponse
from datetime import date, datetime
from .serializers import SupplierSerializer
import json


class SupplierView(APIView):
    """
    API endpoint that allows a device to be viewed.
    """

    serializer_class = SupplierSerializer

    def get(self, request):
        """
        GET a supplier
        rtype: object
        """
        response_data = {}

        if request.user.id is None:
            response_data['error'] = 'Unauthorized'
            response_data['success'] = False
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=401)

        if request.GET.get("id") is None:
            supplier_get = Supplier.objects.all()
            response_data['data'] = SupplierSerializer(supplier_get, many=True).data
            response_data['success'] = True;
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)

        else:
            try:
                supplier_get = Supplier.objects.get(id=request.GET.get("id"))
            except Exception as e:
                response_data['error'] = 'Not found with this pk'
                response_data['success'] = False;
                return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)

            response_data['data'] = SupplierSerializer(supplier_get).data
            response_data['success'] = True;
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)

    def post(self, request):
        """
        POST a supplier
        """
        response_data = {}

        if request.user.id is None:
            response_data['error'] = 'Unauthorized'
            response_data['success'] = False
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=401)

        op = User.objects.get(id=request.user.id)
        user_get = UserSystem.objects.get(user=op)

        if 'title' not in request.data:
            response_data['error'] = 'Not found title'
            response_data['success'] = False
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)
        try:
            supplier_create = Supplier.objects.create(title=request.data["title"], user=user_get,
                                                      last_modified_users=user_get)
        except Exception as e:
            response_data['error'] = 'Duplicated'
            response_data['success'] = False
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)

        response_data['data'] = SupplierSerializer(supplier_create).data
        response_data['success'] = True;
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=201)

    def put(self, request):
        """
        POST a supplier
        """
        response_data = {}

        if request.user.id is None:
            response_data['error'] = 'Unauthorized'
            response_data['success'] = False
            return Response(response_data, status=401)

        op = User.objects.get(id=request.user.id)
        user_get = UserSystem.objects.get(user=op)

        if request.GET.get("id") is None:
            response_data['error'] = 'Not found pk'
            response_data['success'] = False
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)

        if 'title' in request.data:
            try:
                supplier_get = Supplier.objects.get(id=request.GET.get("id"))
                supplier_get.title = request.data["title"]
                supplier_get.last_modified_users = user_get
                supplier_get.last_modified_date = datetime.now()
                supplier_get.save()
            except Exception as e:
                response_data['error'] = 'Not found pk'
                response_data['success'] = False
                return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)
        elif 'delete' in request.data:
            try:
                supplier_get = Supplier.objects.get(id=request.GET.get("id"))
                supplier_get.delete = request.data["delete"]
                supplier_get.last_modified_users = user_get
                supplier_get.last_modified_date = datetime.now()
                supplier_get.save()
            except Exception as e:
                response_data['error'] = 'Not found with this pk'
                response_data['success'] = False
                return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)
        else:
            response_data['error'] = 'Not found any Param'
            response_data['success'] = False
            return Response(response_data, content_type="application/json", status=400)

        response_data['data'] = SupplierSerializer(supplier_get).data
        response_data['success'] = True;
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)

    def delete(self, request):
        """
        POST a supplier.
        """
        response_data = {}

        if request.user.id is None:
            response_data['error'] = 'Unauthorized'
            response_data['success'] = False
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)

        if request.GET.get("id") is None:
            response_data['error'] = 'Not found pk'
            response_data['success'] = False
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)

        try:
            Supplier.objects.filter(id=request.GET.get("id")).delete()
        except Exception as e:
            response_data['success'] = False
            response_data['error'] = 'Not found with this pk'
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)

        response_data['message'] = 'Deleted'
        response_data['success'] = True
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)
