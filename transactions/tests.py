# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from  users.models import UserSystem, UserCategory
from oauth2_provider.models import Application, AccessToken
from rest_framework.test import APITestCase
from datetime import datetime, timedelta
from transactions.models import Supplier
from django.conf import settings
import json


class SupplierTestCase(APITestCase):
    SUPPLIER_URL = '/api/'+ settings.VERSION_API + '/transactions/suppliers/'
    SUPPLIER_URL_DETAIL = '/api/'+ settings.VERSION_API + '/transactions/suppliers/?id={}'
    maxDiff = None

    def setUp(self):
        super(SupplierTestCase, self).setUp()
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

    def test_create_supplier(self):
        data = {
            "title": 'vendorA',
        }

        response = self.client.post(self.SUPPLIER_URL, data, format='json',
                                    HTTP_AUTHORIZATION="Bearer {0}".format(self.tok.token))

        map_response = json.loads(response.content)

        self.assertEquals(response.status_code, 201)

        self.assertEquals(map_response["data"], {
            'title': 'vendorA',
            'delete': False,
            'id': 1,
            'last_modified_users': self.test_user_system.id,
            'user': self.test_user_system.id,
            'last_modified_date': map_response["data"]["last_modified_date"],
        })

    def test_create_supplier_without_authenticate(self):
        data = {
            "title": 'vendorA',
        }

        response = self.client.post(self.SUPPLIER_URL, data, format='json')

        self.assertEquals(response.status_code, 401)

    def test_create_supplier_duplicated(self):
        pref = Supplier.objects.create(
            title='vendorA'
        )

        data = {
            "title": "vendorA",
        }
        response = self.client.post(self.SUPPLIER_URL, data, format='json',
                                    HTTP_AUTHORIZATION="Bearer {0}".format(self.tok.token))

        map_response = json.loads(response.content)

        self.assertEquals(response.status_code, 400)
        self.assertEquals(map_response["success"], False)
        self.assertEquals(map_response['error'], "Duplicated")

    def test_create_supplier_missing_req_field(self):
        data = {

        }

        response = self.client.post(self.SUPPLIER_URL, data, format='json',
                                    HTTP_AUTHORIZATION="Bearer {0}".format(self.tok.token))

        map_response = json.loads(response.content)

        self.assertEquals(response.status_code, 400)
        self.assertEquals(map_response["success"], False)
        self.assertEquals(map_response['error'], "Not found title")

    def test_update_supplier(self):
        old_pref = Supplier.objects.create(
            title='vendorA',
            user=self.test_user_system,
        )

        update_data = {
            "title": "vendorB"
        }

        response = self.client.put(self.SUPPLIER_URL_DETAIL.format(old_pref.id),
                                   update_data,
                                   format='json', HTTP_AUTHORIZATION="Bearer {0}".format(self.tok.token))

        map_response = json.loads(response.content)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(map_response["success"], True)
        self.assertEquals(map_response["data"], {
            'title': 'vendorB',
            'delete': False,
            'id': old_pref.id,
            'last_modified_users': self.test_user_system.id,
            'user': self.test_user_system.id,
            'last_modified_date': map_response["data"]["last_modified_date"],
        })

    def test_soft_delete_supplier(self):
        old_pref = Supplier.objects.create(
            title='vendorA',
            user=self.test_user_system,
        )

        update_data = {
            "delete": True,
        }

        response = self.client.put(self.SUPPLIER_URL_DETAIL.format(old_pref.id),
                                   update_data,
                                   format='json', HTTP_AUTHORIZATION="Bearer {0}".format(self.tok.token))

        map_response = json.loads(response.content)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(map_response["success"], True)
        self.assertEquals(map_response["data"], {
            'title': 'vendorA',
            'delete': True,
            'id': old_pref.id,
            'last_modified_users': self.test_user_system.id,
            'user': self.test_user_system.id,
            'last_modified_date': map_response["data"]["last_modified_date"],
        })

    def test_get_supplier_list(self):
        pref1 = Supplier.objects.create(
            title='vendorA',
            user=self.test_user_system,
        )
        pref2 = Supplier.objects.create(
            title='vendorB',
            user=self.test_user_system,
        )

        response = self.client.get(self.SUPPLIER_URL, format='json',
                                   HTTP_AUTHORIZATION="Bearer {0}".format(self.tok.token))

        self.assertEquals(response.status_code, 200)
        map_response = json.loads(response.content)
        self.assertEquals(len(map_response["data"]), 2)

        self.assertEquals(sorted(map_response["data"][0].keys()), sorted([
            'title', 'delete', 'id', 'user', 'last_modified_users', 'last_modified_date',
        ]))

    def test_get_supplier_specific(self):
        pref = Supplier.objects.create(
            title='vendorA',
            user=self.test_user_system,
            last_modified_users=self.test_user_system
        )

        response = self.client.get(self.SUPPLIER_URL_DETAIL.format(pref.id), format='json',
                                   HTTP_AUTHORIZATION="Bearer {0}".format(self.tok.token))

        map_response = json.loads(response.content)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(map_response["success"], True)
        self.assertEquals(map_response["data"], {
            'title': 'vendorA',
            'delete': False,
            'id': pref.id,
            'last_modified_users': self.test_user_system.id,
            'user': self.test_user_system.id,
            'last_modified_date': map_response["data"]["last_modified_date"],
        })

    def test_delete_supplier(self):
        pref = Supplier.objects.create(
            title='vendorA',
        )

        response = self.client.delete(self.SUPPLIER_URL_DETAIL.format(pref.id), format='json',
                                      HTTP_AUTHORIZATION="Bearer {0}".format(self.tok.token))

        map_response = json.loads(response.content)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(map_response["success"], True)
        self.assertEquals(map_response['message'], "Deleted")
