# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from  users.models import UserSystem, UserCategory
from oauth2_provider.models import Application, AccessToken
from rest_framework.test import APITestCase
from datetime import datetime, timedelta
from products.models import Product, ProductCategory
from  units.models import Unit, UnitCategory
from django.conf import settings
import json


class ProductCategoryTestCase(APITestCase):
    PRODUCT_CATEGORY_URL = '/api/'+ settings.VERSION_API + '/item/product_categories/'
    PRODUCT_CATEGORY_URL_DETAIL = '/api/'+ settings.VERSION_API + '/item/product_categories/?id={}'
    maxDiff = None

    def setUp(self):
        super(ProductCategoryTestCase, self).setUp()
        self.test_user = User.objects.create_user('user1', 'a@a.com', 'qwer1234')
        self.application = Application(
            name="Test Application",
            user=self.test_user,
            client_type=Application.CLIENT_PUBLIC,
            authorization_grant_type=Application.GRANT_PASSWORD,
        )
        self.application.save()
        self.app = Application.objects.get(name="Test Application")
        self.tok = AccessToken.objects.create(
            user=self.test_user, token='1234567890',
            application=self.application, scope='read write',
            expires=datetime.now() + timedelta(days=1)
        )

        self.test_user_category = UserCategory(
            title="shift head",
        )

        self.test_user_category.save()
        self.test_user_system = UserSystem(
            user=self.test_user,
            user_categories=self.test_user_category,
            name='user1_name',
        )
        self.test_user_system.save()

    def test_create_product_category(self):
        data = {
            "title": "Wood",
            "ext_code": "AX01",
        }

        response = self.client.post(self.PRODUCT_CATEGORY_URL, data, format='json',
                                    HTTP_AUTHORIZATION="Bearer {0}".format(self.tok.token))

        map_response = json.loads(response.content)

        self.assertEquals(response.status_code, 201)

        self.assertEquals(map_response["data"], {
            'parent': None,
            'title': "Wood",
            'ext_code':"AX01",
            'delete': False,
            'id': 1,
            'last_modified_users': self.test_user_system.id,
            'user': self.test_user_system.id,
            'last_modified_date': map_response["data"]["last_modified_date"],
        })

    def test_create_product_category_without_authenticate(self):
        data = {
            "title": "Wood",
        }

        response = self.client.post(self.PRODUCT_CATEGORY_URL, data, format='json')

        self.assertEquals(response.status_code, 401)

    def test_create_product_category_duplicated(self):
        pref = ProductCategory.objects.create(
            title='Wood',
            ext_code='AX01'
        )

        data = {
            "title": "Wood",
            "ext_code": "AX01",
        }
        response = self.client.post(self.PRODUCT_CATEGORY_URL, data, format='json',
                                    HTTP_AUTHORIZATION="Bearer {0}".format(self.tok.token))

        map_response = json.loads(response.content)

        self.assertEquals(response.status_code, 400)
        self.assertEquals(map_response["success"], False)
        self.assertEquals(map_response['error'], "Duplicated")

    def test_create_product_category_missing_req_field(self):
        data = {

        }

        response = self.client.post(self.PRODUCT_CATEGORY_URL, data, format='json',
                                    HTTP_AUTHORIZATION="Bearer {0}".format(self.tok.token))

        map_response = json.loads(response.content)

        self.assertEquals(response.status_code, 400)
        self.assertEquals(map_response["success"], False)
        self.assertEquals(map_response['error'], "Not found title")

    def test_update_product_category(self):
        old_pref = ProductCategory.objects.create(
            title="Wood",
            ext_code='AX01',
            user=self.test_user_system
        )

        update_data = {
            "title": "Coco",
            "ext_code" : 'AX01',
        }

        response = self.client.put(self.PRODUCT_CATEGORY_URL_DETAIL.format(old_pref.id),
                                   update_data,
                                   format='json', HTTP_AUTHORIZATION="Bearer {0}".format(self.tok.token))

        map_response = json.loads(response.content)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(map_response["success"], True)
        self.assertEquals(map_response["data"], {
            'title': "Coco",
            'ext_code': "AX01",
            'parent': None,
            'delete': False,
            'id': old_pref.id,
            'last_modified_users': self.test_user_system.id,
            'user': self.test_user_system.id,
            'last_modified_date': map_response["data"]["last_modified_date"],
        })

    def test_soft_delete_product_category(self):
        old_pref = ProductCategory.objects.create(
            title="Wood",
            ext_code='AX01',
            user=self.test_user_system,
            last_modified_users=self.test_user_system
        )

        update_data = {
            "delete": True,
        }

        response = self.client.put(self.PRODUCT_CATEGORY_URL_DETAIL.format(old_pref.id),
                                   update_data,
                                   format='json', HTTP_AUTHORIZATION="Bearer {0}".format(self.tok.token))

        map_response = json.loads(response.content)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(map_response["success"], True)
        self.assertEquals(map_response["data"], {
            'parent': None,
            'title': "Wood",
            'ext_code': "AX01",
            'delete': True,
            'id': old_pref.id,
            'last_modified_users': self.test_user_system.id,
            'user': self.test_user_system.id,
            'last_modified_date': map_response["data"]["last_modified_date"],
        })

    def test_get_product_category_list(self):
        pref1 = ProductCategory.objects.create(
            title="Wood",
            ext_code='AX01',
        )
        pref2 = ProductCategory.objects.create(
            title="Coco",
            ext_code='AX02',
        )

        response = self.client.get(self.PRODUCT_CATEGORY_URL, format='json',
                                   HTTP_AUTHORIZATION="Bearer {0}".format(self.tok.token))

        self.assertEquals(response.status_code, 200)
        map_response = json.loads(response.content)
        self.assertEquals(len(map_response["data"]), 2)

        self.assertEquals(sorted(map_response["data"][0].keys()), sorted([
            'title', 'delete', 'parent','ext_code','id', 'user', 'last_modified_users', 'last_modified_date',
        ]))

    def test_get_product_category_specific(self):
        pref = ProductCategory.objects.create(
            title="Wood",
            ext_code="AX01",
            user=self.test_user_system,
            last_modified_users=self.test_user_system
        )

        response = self.client.get(self.PRODUCT_CATEGORY_URL_DETAIL.format(pref.id), format='json',
                                   HTTP_AUTHORIZATION="Bearer {0}".format(self.tok.token))

        map_response = json.loads(response.content)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(map_response["success"], True)
        self.assertEquals(map_response["data"], {
            'parent': None,
            'title': "Wood",
            'ext_code' : "AX01",
            'delete': False,
            'id': pref.id,
            'last_modified_users': self.test_user_system.id,
            'user': self.test_user_system.id,
            'last_modified_date': map_response["data"]["last_modified_date"],
        })

    def test_delete_product_category(self):
        pref = ProductCategory.objects.create(
            ext_code="AX01",
            title="Wood"
        )

        response = self.client.delete(self.PRODUCT_CATEGORY_URL_DETAIL.format(pref.id), format='json',
                                      HTTP_AUTHORIZATION="Bearer {0}".format(self.tok.token))

        map_response = json.loads(response.content)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(map_response["success"], True)
        self.assertEquals(map_response['message'], "Deleted")


class ProductTestCase(APITestCase):
    PRODUCT_URL = '/api/'+ settings.VERSION_API + '/item/products/'
    PRODUCT_URL_DETAIL = '/api/'+ settings.VERSION_API + '/item/products/?id={}'
    maxDiff = None

    def setUp(self):
        super(ProductTestCase, self).setUp()
        self.test_user = User.objects.create_user('user1', 'a@a.com', 'qwer1234')
        self.application = Application(
            name="Test Application",
            user=self.test_user,
            client_type=Application.CLIENT_PUBLIC,
            authorization_grant_type=Application.GRANT_PASSWORD,
        )
        self.application.save()
        self.app = Application.objects.get(name="Test Application")
        self.tok = AccessToken.objects.create(
            user=self.test_user, token='1234567890',
            application=self.application, scope='read write',
            expires=datetime.now() + timedelta(days=1)
        )

        self.test_user_category = UserCategory(
            title="shift head",
        )

        self.test_user_category.save()
        self.test_user_system = UserSystem(
            user=self.test_user,
            user_categories=self.test_user_category,
            name='user1_name',
        )
        self.test_user_system.save()

        self.product_category = ProductCategory.objects.create(
            title='Wood',
        )

        self.unit_category = UnitCategory.objects.create(
            title="weights"
        )

        self.units = Unit.objects.create(
            title='kilograms',
            types=1,
            ratio=20,
            units_categories=self.unit_category
        )

    def test_create_product(self):
        data = {
            "title": "Wood_1",
            "product_categories": self.product_category.id,
            "units": self.units.id,
            "quantity": 10,
            "stockable": True,
        }

        response = self.client.post(self.PRODUCT_URL, data, format='json',
                                    HTTP_AUTHORIZATION="Bearer {0}".format(self.tok.token))

        map_response = json.loads(response.content)

        self.assertEquals(response.status_code, 201)

        self.assertEquals(map_response["data"], {
            'title': "Wood_1",
            'product_categories': self.product_category.id,
            'units': self.units.id,
            'quantity': 10,
            'stockable': True,
            'delete': False,
            'id': 1,
            'last_modified_users': self.test_user_system.id,
            'user': self.test_user_system.id,
            'last_modified_date': map_response["data"]["last_modified_date"],
        })

    def test_create_product_without_authenticate(self):
        data = {
            "title": "Wood_1",
            "product_categories": self.product_category.id,
            "units": self.units.id,
            "quantity": 10,
            "stockable": True,
        }

        response = self.client.post(self.PRODUCT_URL, data, format='json')

        self.assertEquals(response.status_code, 401)

    def test_create_product_duplicated(self):
        pref = Product.objects.create(
            title='Wood_1',
            product_categories=self.product_category,
            units=self.units,
            quantity=10,
            stockable=True,
        )

        data = {
            "title": "Wood_1",
            "product_categories": self.product_category.id,
            "units": self.units.id,
            "quantity": 10,
            "stockable": True,
        }
        response = self.client.post(self.PRODUCT_URL, data, format='json',
                                    HTTP_AUTHORIZATION="Bearer {0}".format(self.tok.token))

        map_response = json.loads(response.content)

        self.assertEquals(response.status_code, 400)
        self.assertEquals(map_response["success"], False)
        self.assertEquals(map_response['error'], "Duplicated")

    def test_create_product_missing_req_field(self):
        data = {
            "title": "Wood_1",
            "product_categories": self.product_category.id,
        }

        response = self.client.post(self.PRODUCT_URL, data, format='json',
                                    HTTP_AUTHORIZATION="Bearer {0}".format(self.tok.token))

        map_response = json.loads(response.content)

        self.assertEquals(response.status_code, 400)
        self.assertEquals(map_response["success"], False)
        self.assertEquals(map_response['error'], "Need more data")

    def test_update_product(self):
        old_pref = Product.objects.create(
            title='Wood_1',
            product_categories=self.product_category,
            units=self.units,
            quantity=10,
            stockable=True,
            user=self.test_user_system,
        )

        update_data = {
            "title": 'Wood_2',
            "product_categories": self.product_category.id,
            "units": self.units.id,
            "quantity": 10,
            "stockable": True,
        }

        response = self.client.put(self.PRODUCT_URL_DETAIL.format(old_pref.id),
                                   update_data,
                                   format='json', HTTP_AUTHORIZATION="Bearer {0}".format(self.tok.token))

        map_response = json.loads(response.content)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(map_response["success"], True)
        self.assertEquals(map_response["data"], {
            'title': "Wood_2",
            'product_categories': self.product_category.id,
            'units': self.units.id,
            'quantity': 10,
            'stockable': True,
            'delete': False,
            'id': 1,
            'last_modified_users': self.test_user_system.id,
            'user': self.test_user_system.id,
            'last_modified_date': map_response["data"]["last_modified_date"],
        })

    def test_soft_delete_product(self):
        old_pref = Product.objects.create(
            title='Wood_1',
            product_categories=self.product_category,
            units=self.units,
            quantity=10,
            stockable=True,
            user=self.test_user_system
        )

        update_data = {
            "delete": True,
        }

        response = self.client.put(self.PRODUCT_URL_DETAIL.format(old_pref.id),
                                   update_data,
                                   format='json', HTTP_AUTHORIZATION="Bearer {0}".format(self.tok.token))

        map_response = json.loads(response.content)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(map_response["success"], True)
        self.assertEquals(map_response["data"], {
            'title': "Wood_1",
            'product_categories': self.product_category.id,
            'units': self.units.id,
            'quantity': 10,
            'stockable': True,
            'delete': True,
            'id': 1,
            'last_modified_users': self.test_user_system.id,
            'user': self.test_user_system.id,
            'last_modified_date': map_response["data"]["last_modified_date"],
        })

    def test_get_product_list(self):
        pref1 = Product.objects.create(
            title='Wood_1',
            product_categories=self.product_category,
            units=self.units,
            quantity=10,
            stockable=True,
        )
        pref2 = Product.objects.create(
            title='Wood_2',
            product_categories=self.product_category,
            units=self.units,
            quantity=10,
            stockable=True,
        )

        response = self.client.get(self.PRODUCT_URL, format='json',
                                   HTTP_AUTHORIZATION="Bearer {0}".format(self.tok.token))

        self.assertEquals(response.status_code, 200)
        map_response = json.loads(response.content)
        self.assertEquals(len(map_response["data"]), 2)

        self.assertEquals(sorted(map_response["data"][0].keys()), sorted([
            'title', 'delete', 'units', 'product_categories', 'stockable', 'quantity', 'id', 'user',
            'last_modified_users', 'last_modified_date',
        ]))

    def test_get_product_specific(self):
        pref = Product.objects.create(
            title='Wood_1',
            product_categories=self.product_category,
            units=self.units,
            quantity=10,
            stockable=True,
            user=self.test_user_system,
            last_modified_users=self.test_user_system,
        )

        response = self.client.get(self.PRODUCT_URL_DETAIL.format(pref.id), format='json',
                                   HTTP_AUTHORIZATION="Bearer {0}".format(self.tok.token))

        map_response = json.loads(response.content)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(map_response["success"], True)
        self.assertEquals(map_response["data"], {
            'title': "Wood_1",
            'product_categories': self.product_category.id,
            'units': self.units.id,
            'quantity': 10,
            'stockable': True,
            'delete': False,
            'id': 1,
            'last_modified_users': self.test_user_system.id,
            'user': self.test_user_system.id,
            'last_modified_date': map_response["data"]["last_modified_date"],
        })

    def test_delete_product(self):
        pref = Product.objects.create(
            title='Wood_1',
            product_categories=self.product_category,
            units=self.units,
            quantity=10,
            stockable=True,
        )

        response = self.client.delete(self.PRODUCT_URL_DETAIL.format(pref.id), format='json',
                                      HTTP_AUTHORIZATION="Bearer {0}".format(self.tok.token))

        map_response = json.loads(response.content)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(map_response["success"], True)
        self.assertEquals(map_response['message'], "Deleted")
