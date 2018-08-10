from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Shift
from users.models import UserSystem
from rest_framework import status
from django.http import HttpResponse
from datetime import date, datetime
from .serializers import ShiftSerializer
import json


class ShiftView(APIView):
    """
    API endpoint that allows a device to be viewed.
    """

    serializer_class = ShiftSerializer

    def get(self, request):
        """
        GET a shift
        :rtype: object
        """

        response_data = {}

        if request.user.id is None:
            response_data['error'] = 'Unauthorized'
            response_data['success'] = False
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=401)

        if request.GET.get("id") is None:
            shift_get = Shift.objects.all()
            response_data['data'] = ShiftSerializer(shift_get, many=True).data
            response_data['success'] = True;
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)
        else:
            try:
                shifts_get = Shift.objects.get(id=request.GET.get("id"))
            except Exception as e:
                response_data['error'] = 'Not found with this pk'
                response_data['success'] = False;
                return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)

            response_data['data'] = ShiftSerializer(shifts_get).data
            response_data['success'] = True;
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)

    def post(self, request):
        """
        POST a shift
        """
        response_data = {}

        if request.user.id is None:
            response_data['error'] = 'Unauthorized'
            response_data['success'] = False
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=401)

        op = User.objects.get(id=request.user.id)
        user_get = UserSystem.objects.get(user=op)

        if 'title' not in request.data or 'description' not in request.data:
            response_data['error'] = 'Not found title or description'
            response_data['success'] = False
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)
        try:
            shifts_create = Shift.objects.create(title=request.data["title"], description=request.data["description"],
                                                 user=user_get, last_modified_users=user_get)
        except Exception as e:
            response_data['error'] = 'Duplicated'
            response_data['success'] = False
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)

        response_data['data'] = ShiftSerializer(shifts_create).data
        response_data['success'] = True;
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=201)

    def put(self, request):
        """
        POST a customer.
        """
        response_data = {}

        if request.user.id is None:
            response_data['error'] = 'Unauthorized'
            response_data['success'] = False
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=401)

        op = User.objects.get(id=request.user.id)
        user_get = UserSystem.objects.get(user=op)

        if request.GET.get("id") is None:
            response_data['error'] = 'Not found pk'
            response_data['success'] = False
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)

        if 'title' in request.data and 'description' in request.data:
            try:
                shifts_get = Shift.objects.get(id=request.GET.get("id"))
                shifts_get.title = request.data["title"]
                shifts_get.description = request.data["description"]
                shifts_get.last_modified_users = user_get
                shifts_get.last_modified_date = datetime.now()
                shifts_get.save()
            except Exception as e:
                response_data['error'] = 'Not found pk'
                response_data['success'] = False
                return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)
        elif 'delete' in request.data:
            try:
                shifts_get = Shift.objects.get(id=request.GET.get("id"))
                shifts_get.delete = request.data["delete"]
                shifts_get.last_modified_users = user_get
                shifts_get.last_modified_date = datetime.now()
                shifts_get.save()
            except Exception as e:
                response_data['error'] = 'Not found with this pk'
                response_data['success'] = False
                return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)
        else:
            response_data['error'] = 'Not found any Param'
            response_data['success'] = False
            return Response(response_data, content_type="application/json", status=400)

        response_data['data'] = ShiftSerializer(shifts_get).data
        response_data['success'] = True;
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)

    def delete(self, request):
        """
        POST a shift.
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
            Shift.objects.filter(id=request.GET.get("id")).delete()
        except Exception as e:
            response_data['success'] = False
            response_data['error'] = 'Not found with this pk'
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)

        response_data['message'] = 'Deleted'
        response_data['success'] = True
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)
