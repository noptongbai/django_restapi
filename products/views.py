from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ProductCategory, Product
from users.models import UserSystem
from rest_framework import status
from django.http import HttpResponse
from datetime import date, datetime
from .serializers import ProductCategorySerializer, ProductSerializer, ProductWithCategoryTitleSerializer
import json


class ProductCategoryView(APIView):
    """
    API endpoint that allows a device to be viewed.
    """

    serializer_class = ProductCategorySerializer

    def get(self, request):
        """
        GET a product_categories
        :rtype: object
        """
        response_data = {}

        if request.user.id is None:
            response_data['error'] = 'Unauthorized'
            response_data['success'] = False
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=401)

        if request.GET.get("id") is None:
            product_categories_get = ProductCategory.objects.all()
            response_data['data'] = ProductCategorySerializer(product_categories_get, many=True).data
            response_data['success'] = True;
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)

        else:
            try:
                product_categories_get = ProductCategory.objects.get(id=request.GET.get("id"))
            except Exception as e:
                response_data['error'] = 'Not found with this pk'
                response_data['success'] = False;
                return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)

            response_data['data'] = ProductCategorySerializer(product_categories_get).data
            response_data['success'] = True;
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)

    def post(self, request):
        """
        POST a product_categories
        """
        response_data = {}

        if request.user.id is None:
            response_data['error'] = 'Unauthorized'
            response_data['success'] = False
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=401)

        op = User.objects.get(id=request.user.id)
        user_get = UserSystem.objects.get(user=op)

        if 'title' not in request.data or 'ext_code' not in request.data:
            response_data['error'] = 'Not found title'
            response_data['success'] = False
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)
        try:
            product_categories_create = ProductCategory.objects.create(title=request.data["title"],
                                                                       ext_code=request.data["ext_code"]
                                                                       , user=user_get,
                                                                       last_modified_users=user_get)
        except Exception as e:
            response_data['error'] = 'Duplicated'
            response_data['success'] = False
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)

        response_data['data'] = ProductCategorySerializer(product_categories_create).data
        response_data['success'] = True;
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=201)

    def put(self, request):
        """
        POST a product_categories.
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

        if 'title' in request.data and 'ext_code' in request.data:
            try:
                product_categories_get = ProductCategory.objects.get(id=request.GET.get("id"))
                product_categories_get.title = request.data["title"]
                product_categories_get.ext_code = request.data["ext_code"]
                product_categories_get.last_modified_users = user_get
                product_categories_get.last_modified_date = datetime.now()
                product_categories_get.save()
            except Exception as e:
                response_data['error'] = 'Not found pk'
                response_data['success'] = False
                return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)
        elif 'delete' in request.data:
            try:
                product_categories_get = ProductCategory.objects.get(id=request.GET.get("id"))
                product_categories_get.delete = request.data["delete"]
                product_categories_get.save()
            except Exception as e:
                response_data['error'] = 'Not found with this pk'
                response_data['success'] = False
                return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)
        else:
            response_data['error'] = 'Not found any Param'
            response_data['success'] = False
            return Response(response_data, content_type="application/json", status=400)

        response_data['data'] = ProductCategorySerializer(product_categories_get).data
        response_data['success'] = True;
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)

    def delete(self, request):
        """
        POST a product_categories.
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
            ProductCategory.objects.filter(id=request.GET.get("id")).delete()
        except Exception as e:
            response_data['success'] = False
            response_data['error'] = 'Not found with this pk'
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)

        response_data['message'] = 'Deleted'
        response_data['success'] = True
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)


class ProductView(APIView):
    """
    API endpoint that allows a device to be viewed.
    """

    serializer_class = ProductSerializer

    def get(self, request):
        """
        GET a product_categories
        :rtype: object
        """
        response_data = {}

        if request.user.id is None:
            response_data['error'] = 'Unauthorized'
            response_data['success'] = False
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=401)

        if request.GET.get("id") is None:
            product_get = Product.objects.all()
            response_data['data'] = ProductWithCategoryTitleSerializer(product_get, many=True).data
            response_data['success'] = True;
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)

        else:
            try:
                product_get = Product.objects.get(id=request.GET.get("id"))
            except Exception as e:
                response_data['error'] = 'Not found with this pk'
                response_data['success'] = False;
                return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)

            response_data['data'] = ProductWithCategoryTitleSerializer(product_get).data
            response_data['success'] = True;
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)

    def post(self, request):
        """
        POST a product_categories
        """
        response_data = {}

        if request.user.id is None:
            response_data['error'] = 'Unauthorized'
            response_data['success'] = False
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=401)

        op = User.objects.get(id=request.user.id)
        user_get = UserSystem.objects.get(user=op)

        if 'title' not in request.data or 'product_categories' not in request.data or 'quantity' not in request.data or 'units' not in request.data or 'stockable' not in request.data:
            response_data['error'] = 'Need more data'
            response_data['success'] = False
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)
        try:
            product_create = Product.objects.create(title=request.data["title"], user=user_get,
                                                    product_categories_id=request.data["product_categories"],
                                                    units_id=request.data["units"],
                                                    quantity=request.data["quantity"],
                                                    stockable=request.data["stockable"],
                                                    last_modified_users=user_get)
        except Exception as e:
            print(e)
            response_data['error'] = 'Duplicated'
            response_data['success'] = False
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)

        response_data['data'] = ProductWithCategoryTitleSerializer(product_create).data
        response_data['success'] = True;
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=201)

    def put(self, request):
        """
        POST a product_categories.
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

        if 'title' in request.data and 'product_categories' in request.data and 'quantity' in request.data and 'units' in request.data and 'stockable' in request.data:
            try:
                product_get = Product.objects.get(id=request.GET.get("id"))
                try:
                    product_get.title = request.data["title"]
                    product_get.product_categories_id = request.data["product_categories"]
                    product_get.quantity = request.data["quantity"]
                    product_get.stockable = request.data["stockable"]
                    product_get.units_id = request.data["units"]
                    product_get.last_modified_users = user_get
                    product_get.last_modified_date = datetime.now()
                    product_get.save()
                except Exception as e:
                    print (e)
                    response_data['error'] = 'Duplicated'
                    response_data['success'] = False
                    return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)

            except Exception as e:
                print (e)
                response_data['error'] = 'Not found pk'
                response_data['success'] = False
                return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)

        elif 'delete' in request.data:
            try:
                product_get = Product.objects.get(id=request.GET.get("id"))
                product_get.delete = request.data["delete"]
                product_get.last_modified_users = user_get
                product_get.last_modified_date = datetime.now()
                product_get.save()
            except Exception as e:
                response_data['error'] = 'Not found with this pk'
                response_data['success'] = False
                return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)
        else:
            response_data['error'] = 'Not found any Param'
            response_data['success'] = False
            return Response(response_data, content_type="application/json", status=400)

        response_data['data'] = ProductWithCategoryTitleSerializer(product_get).data
        response_data['success'] = True;
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)

    def delete(self, request):
        """
        POST a product_categories.
        """
        response_data = {}

        if request.user.id is None:
            response_data['error'] = 'Unauthorized'
            response_data['success'] = False
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)
            r

        if request.GET.get("id") is None:
            response_data['error'] = 'Not found pk'
            response_data['success'] = False
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)

        try:
            Product.objects.filter(id=request.GET.get("id")).delete()
        except Exception as e:
            response_data['success'] = False
            response_data['error'] = 'Not found with this pk'
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)

        response_data['message'] = 'Deleted'
        response_data['success'] = True
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)
