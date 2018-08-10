from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Unit, UnitCategory
from users.models import UserSystem
from rest_framework import status
from django.http import HttpResponse
from datetime import date, datetime
from .serializers import UnitCategorySerializer, UnitSerializer,UnitWithCategoryTitleSerializer
import json


class UnitCategoryView(APIView):
    """
    API endpoint that allows a device to be viewed.
    """

    serializer_class = UnitCategorySerializer

    def get(self, request):
        """
        GET a units_category
        :rtype: object
        """
        response_data = {}

        if request.user.id is None:
            response_data['error'] = 'Unauthorized'
            response_data['success'] = False
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=401)

        if request.GET.get("id") is None:
            units_categories_get = UnitCategory.objects.all()
            response_data['data'] = UnitCategorySerializer(units_categories_get, many=True).data
            response_data['success'] = True;
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)
        else:
            try:
                units_categories_get = UnitCategory.objects.get(id=request.GET.get("id"))
            except Exception as e:
                response_data['error'] = 'Not found with this pk'
                response_data['success'] = False;
                return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)

            response_data['data'] = (UnitCategorySerializer(units_categories_get).data)
            response_data['success'] = True;
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)

    def post(self, request):
        """
        POST a units_category
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
            units_categories_create = UnitCategory.objects.create(title=request.data["title"], user=user_get,
                                                                  last_modified_users=user_get)
        except Exception as e:
            response_data['error'] = 'Duplicated'
            response_data['success'] = False
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)

        response_data['data'] = UnitCategorySerializer(units_categories_create).data
        response_data['success'] = True;
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=201)

    def put(self, request):
        """
        POST a units_category.
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
                units_categories_get = UnitCategory.objects.get(id=request.GET.get("id"))
                units_categories_get.title = request.data["title"]
                units_categories_get.last_modified_users = user_get
                units_categories_get.last_modified_date = datetime.now()
                units_categories_get.save()
            except Exception as e:
                response_data['error'] = 'Not found pk'
                response_data['success'] = False
                return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)
        elif 'delete' in request.data:
            try:
                units_categories_get = UnitCategory.objects.get(id=request.GET.get("id"))
                units_categories_get.delete = request.data["delete"]
                units_categories_get.last_modified_users = user_get
                units_categories_get.last_modified_date = datetime.now()
                units_categories_get.save()
            except Exception as e:
                response_data['error'] = 'Not found with this pk'
                response_data['success'] = False
                return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)
        else:
            response_data['error'] = 'Not found any Param'
            response_data['success'] = False
            return Response(response_data, content_type="application/json", status=400)

        response_data['data'] = UnitCategorySerializer(units_categories_get).data
        response_data['success'] = True;
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)

    def delete(self, request):
        """
        DELETE a units_category.
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
            UnitCategory.objects.filter(id=request.GET.get("id")).delete()
        except Exception as e:
            response_data['success'] = False
            response_data['error'] = 'Not found with this pk'
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)

        response_data['message'] = 'Deleted'
        response_data['success'] = True
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)


class UnitView(APIView):
    """
    API endpoint that allows a device to be viewed.
    """

    serializer_class = UnitSerializer

    def get(self, request):
        """
        GET a units_category
        :rtype: object
        """
        response_data = {}

        if request.user.id is None:
            response_data['error'] = 'Unauthorized'
            response_data['success'] = False
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=401)

        if request.GET.get("id") is None:
            units_get = Unit.objects.all()
            response_data['data'] = UnitWithCategoryTitleSerializer(units_get, many=True).data
            response_data['success'] = True;
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)
        else:
            try:
                units_get = Unit.objects.get(id=request.GET.get("id"))
            except Exception as e:
                response_data['error'] = 'Not found with this pk'
                response_data['success'] = False;
                return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)

            response_data['data'] = (UnitWithCategoryTitleSerializer(units_get).data)
            response_data['success'] = True;
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)

    def post(self, request):
        """
        POST a units_category
        """
        response_data = {}

        if request.user.id is None:
            response_data['error'] = 'Unauthorized'
            response_data['success'] = False
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=401)

        op = User.objects.get(id=request.user.id)
        user_get = UserSystem.objects.get(user=op)

        if 'title' not in request.data or 'units_categories' not in request.data or 'types' not in request.data or 'ratio' not in request.data:
            response_data['error'] = 'Need more data'
            response_data['success'] = False
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)
        try:
            units_create = Unit.objects.create(title=request.data["title"], user=user_get,
                                               units_categories_id=request.data["units_categories"],
                                               types=request.data["types"], ratio=request.data["ratio"],
                                               last_modified_users=user_get)
        except Exception as e:
            response_data['error'] = 'Duplicated'
            response_data['success'] = False
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)

        response_data['data'] = UnitWithCategoryTitleSerializer(units_create).data
        response_data['success'] = True;
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=201)

    def put(self, request):
        """
        POST a units_category.
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

        if 'title' in request.data and 'ratio' in request.data and 'units_categories' in request.data and 'types' in request.data:
            try:
                units_get = Unit.objects.get(id=request.GET.get("id"))
                units_get.title = request.data["title"]
                units_get.units_categories.id = request.data["units_categories"]
                units_get.types = request.data["types"]
                units_get.ratio = request.data["ratio"]
                units_get.last_modified_users = user_get
                units_get.last_modified_date = datetime.now()
                units_get.save()
            except Exception as e:
                response_data['error'] = 'Not found with this pk'
                response_data['success'] = False
                return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)
        elif 'delete' in request.data:
            try:
                units_get = Unit.objects.get(id=request.GET.get("id"))
                units_get.delete = request.data["delete"]
                units_get.last_modified_users = user_get
                units_get.last_modified_date = datetime.now()
                units_get.save()
            except Exception as e:
                response_data['error'] = 'Not found with this pk'
                response_data['success'] = False
                return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)
        else:
            response_data['error'] = 'Not found any Param'
            response_data['success'] = False
            return Response(response_data, content_type="application/json", status=400)

        response_data['data'] = UnitWithCategoryTitleSerializer(units_get).data
        response_data['success'] = True;
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)

    def delete(self, request):
        """
        DELETE a units_category.
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
            Unit.objects.filter(id=request.GET.get("id")).delete()
        except Exception as e:
            response_data['success'] = False
            response_data['error'] = 'Not found with this pk'
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)

        response_data['message'] = 'Deleted'
        response_data['success'] = True
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)
