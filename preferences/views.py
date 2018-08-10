from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Preference
from  users.models import UserCategory, UserSystem
from rest_framework import status
from .serializers import PreferenceSerializer
from django.http import HttpResponse
from datetime import date, datetime
from django.db import IntegrityError
import json


class PreferencesView(APIView):
    """
    API endpoint that allows a device to be viewed.
    """

    serializer_class = PreferenceSerializer

    def get(self, request, ):
        """
        GET a preferences
        :rtype: object
        """
        response_data = {}

        if request.user.id is None:
            response_data['error'] = 'Unauthorized'
            response_data['success'] = False
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=401)

        if request.GET.get("id") is None:
            preferences_get = Preference.objects.all()
            response_data['data'] = PreferenceSerializer(preferences_get, many=True).data
            response_data['success'] = True;
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)

        else:
            try:
                preferences_get = Preference.objects.get(id=request.GET.get("id"))
            except Exception as e:
                response_data['error'] = 'Not found with this pk'
                response_data['success'] = False;
                return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)

            response_data['data'] = PreferenceSerializer(preferences_get).data
            response_data['success'] = True;
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)

    def post(self, request):
        """
        POST a preferences
        """
        response_data = {}

        if request.user.id is None:
            response_data['error'] = 'Unauthorized'
            response_data['success'] = False
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=401)

        op = User.objects.get(id=request.user.id)
        user_get = UserSystem.objects.get(user=op)

        if 'key' not in request.data or 'value' not in request.data or 'description' not in request.data:
            response_data['error'] = 'Not found key or value or description'
            response_data['success'] = False
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)
        try:
            preferences_create = Preference.objects.create(key=request.data["key"], value=request.data["value"],
                                                           description=request.data["description"], user=user_get,
                                                           last_modified_users=user_get)
        except IntegrityError as e:
            response_data['error'] = 'Duplicated'
            response_data['success'] = False
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)
        except Exception as b:
            response_data['error'] = 'Wrong Input'
            response_data['success'] = False
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)

        response_data['data'] = PreferenceSerializer(preferences_create).data
        response_data['success'] = True;
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=201)

    def put(self, request):
        """
        POST a preferences
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

        if 'key' in request.data and 'value' in request.data and 'description' in request.data:
            try:
                preferences_get = Preference.objects.get(id=request.GET.get("id"))
                preferences_get.key = request.data["key"]
                preferences_get.value = request.data["value"]
                preferences_get.description = request.data["description"]
                preferences_get.last_modified_users = user_get
                preferences_get.last_modified_date = datetime.now()
                preferences_get.save()
            except Exception as e:
                response_data['error'] = 'Not found pk'
                response_data['success'] = False
                return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)
        elif 'delete' in request.data:
            try:
                preferences_get = Preference.objects.get(id=request.GET.get("id"))
                preferences_get.delete = request.data["delete"]
                preferences_get.last_modified_users = user_get
                preferences_get.last_modified_date = datetime.now()
                preferences_get.save()
            except Exception as e:
                response_data['error'] = 'Not found with this pk'
                response_data['success'] = False
                return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)
        else:
            response_data['error'] = 'Not found any Param'
            response_data['success'] = False
            return Response(response_data, content_type="application/json", status=400)

        response_data['data'] = PreferenceSerializer(preferences_get).data
        response_data['success'] = True;
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)

    def delete(self, request):
        """
        POST a preferences
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
            Preference.objects.filter(id=request.GET.get("id")).delete()
        except Exception as e:
            response_data['success'] = False
            response_data['error'] = 'Not found with this pk'
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)

        response_data['message'] = 'Deleted'
        response_data['success'] = True
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)
