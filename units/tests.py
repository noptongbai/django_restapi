# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from  users.models import UserSystem, UserCategory
from oauth2_provider.models import Application, AccessToken
from rest_framework.test import APITestCase
from datetime import datetime, timedelta
from units.models import Unit, UnitCategory
from django.conf import settings
import json


class UnitCategoryTestCase(APITestCase):
    UNIT_CATEGORY_URL = '/api/'+ settings.VERSION_API + '/uom/units_categories/'
    UNIT_CATEGORY_URL_DETAIL = '/api/'+ settings.VERSION_API + '/uom/units_categories/?id={}'
    maxDiff = None

    def setUp(self):
        super(UnitCategoryTestCase, self).setUp()
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

    def test_create_unit_category(self):
        data = {
            "title": 'weights',
        }

        response = self.client.post(self.UNIT_CATEGORY_URL, data, format='json',
                                    HTTP_AUTHORIZATION="Bearer {0}".format(self.tok.token))

        map_response = json.loads(response.content)

        self.assertEquals(response.status_code, 201)

        self.assertEquals(map_response["data"], {
            'parent': None,
            'title': 'weights',
            'delete': False,
            'id': 1,
            'last_modified_users': self.test_user_system.id,
            'user': self.test_user_system.id,
            'last_modified_date': map_response["data"]["last_modified_date"],
        })

    def test_create_unit_category_without_authenticate(self):
        data = {
            "title": 'weights',
        }

        response = self.client.post(self.UNIT_CATEGORY_URL, data, format='json')

        self.assertEquals(response.status_code, 401)

    def test_create_unit_category_duplicated(self):
        pref = UnitCategory.objects.create(
            title='weights'
        )

        data = {
            "title": "weights",
        }
        response = self.client.post(self.UNIT_CATEGORY_URL, data, format='json',
                                    HTTP_AUTHORIZATION="Bearer {0}".format(self.tok.token))

        map_response = json.loads(response.content)

        self.assertEquals(response.status_code, 400)
        self.assertEquals(map_response["success"], False)
        self.assertEquals(map_response['error'], "Duplicated")

    def test_create_unit_category_missing_req_field(self):
        data = {

        }

        response = self.client.post(self.UNIT_CATEGORY_URL, data, format='json',
                                    HTTP_AUTHORIZATION="Bearer {0}".format(self.tok.token))

        map_response = json.loads(response.content)

        self.assertEquals(response.status_code, 400)
        self.assertEquals(map_response["success"], False)
        self.assertEquals(map_response['error'], "Not found title")

    def test_update_unit_category(self):
        old_pref = UnitCategory.objects.create(
            title='weights',
            user=self.test_user_system,
        )

        update_data = {
            "title": "weights"
        }

        response = self.client.put(self.UNIT_CATEGORY_URL_DETAIL.format(old_pref.id),
                                   update_data,
                                   format='json', HTTP_AUTHORIZATION="Bearer {0}".format(self.tok.token))

        map_response = json.loads(response.content)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(map_response["success"], True)
        self.assertEquals(map_response["data"], {
            'parent': None,
            'title': 'weights',
            'delete': False,
            'id': old_pref.id,
            'last_modified_users': self.test_user_system.id,
            'user': self.test_user_system.id,
            'last_modified_date': map_response["data"]["last_modified_date"],
        })

    def test_soft_delete_unit_category(self):
        old_pref = UnitCategory.objects.create(
            title='weights',
            user=self.test_user_system,
        )

        update_data = {
            "delete": True,
        }

        response = self.client.put(self.UNIT_CATEGORY_URL_DETAIL.format(old_pref.id),
                                   update_data,
                                   format='json', HTTP_AUTHORIZATION="Bearer {0}".format(self.tok.token))

        map_response = json.loads(response.content)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(map_response["success"], True)
        self.assertEquals(map_response["data"], {
            'parent': None,
            'title': 'weights',
            'delete': True,
            'id': old_pref.id,
            'last_modified_users': self.test_user_system.id,
            'user': self.test_user_system.id,
            'last_modified_date': map_response["data"]["last_modified_date"],
        })

    def test_get_unit_category_list(self):
        pref1 = UnitCategory.objects.create(
            title='weights',
            user=self.test_user_system,
        )
        pref2 = UnitCategory.objects.create(
            title='heights',
            user=self.test_user_system,
        )

        response = self.client.get(self.UNIT_CATEGORY_URL, format='json',
                                   HTTP_AUTHORIZATION="Bearer {0}".format(self.tok.token))

        self.assertEquals(response.status_code, 200)
        map_response = json.loads(response.content)
        self.assertEquals(len(map_response["data"]), 2)

        self.assertEquals(sorted(map_response["data"][0].keys()), sorted([
            'parent', 'title', 'delete', 'id', 'user', 'last_modified_users', 'last_modified_date',
        ]))

    def test_get_unit_category_specific(self):
        pref = UnitCategory.objects.create(
            title='weights',
            user=self.test_user_system,
            last_modified_users=self.test_user_system
        )

        response = self.client.get(self.UNIT_CATEGORY_URL_DETAIL.format(pref.id), format='json',
                                   HTTP_AUTHORIZATION="Bearer {0}".format(self.tok.token))

        map_response = json.loads(response.content)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(map_response["success"], True)
        self.assertEquals(map_response["data"], {
            'parent': None,
            'title': 'weights',
            'delete': False,
            'id': pref.id,
            'last_modified_users': self.test_user_system.id,
            'user': self.test_user_system.id,
            'last_modified_date': map_response["data"]["last_modified_date"],
        })

    def test_delete_unit_category(self):
        pref = UnitCategory.objects.create(
            title='weights',
        )

        response = self.client.delete(self.UNIT_CATEGORY_URL_DETAIL.format(pref.id), format='json',
                                      HTTP_AUTHORIZATION="Bearer {0}".format(self.tok.token))

        map_response = json.loads(response.content)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(map_response["success"], True)
        self.assertEquals(map_response['message'], "Deleted")


class UnitTestCase(APITestCase):
    UNIT_URL = '/api/'+ settings.VERSION_API + '/uom/units/'
    UNIT_URL_DETAIL = '/api/'+ settings.VERSION_API + '/uom/units/?id={}'
    maxDiff = None

    def setUp(self):
        super(UnitTestCase, self).setUp()
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

    def test_create_unit(self):
        self.unit_category = UnitCategory.objects.create(
            title='weights'
        )

        data = {
            "title": 'kilograms',
            "types": 2,
            "ratio": 20,
            "units_categories": self.unit_category.id,
        }

        response = self.client.post(self.UNIT_URL, data, format='json',
                                    HTTP_AUTHORIZATION="Bearer {0}".format(self.tok.token))

        map_response = json.loads(response.content)

        self.assertEquals(response.status_code, 201)

        self.assertEquals(map_response["data"], {
            'title': 'kilograms',
            'units_categories': self.unit_category.id,
            "types": 2,
            "ratio": 20,
            'delete': False,
            'id': 1,
            'last_modified_users': self.test_user_system.id,
            'user': self.test_user_system.id,
            'last_modified_date': map_response["data"]["last_modified_date"],
        })

    def test_create_unit_without_authenticate(self):
        self.unit_category = UnitCategory.objects.create(
            title='weights'
        )

        data = {
            "title": 'kilograms',
            "types": 2,
            "ratio": 20,
            "units_categories": self.unit_category.id,
        }

        response = self.client.post(self.UNIT_URL, data, format='json')

        self.assertEquals(response.status_code, 401)

    def test_create_unit_duplicated(self):
        self.unit_category = UnitCategory.objects.create(
            title='weights'
        )
        pref = Unit.objects.create(
            title='kilograms',
            types=2,
            ratio=20,
            units_categories=self.unit_category,
        )

        data = {
            "title": 'kilograms',
            "types": 2,
            "ratio": 20,
            "units_categories": self.unit_category.id,
        }
        response = self.client.post(self.UNIT_URL, data, format='json',
                                    HTTP_AUTHORIZATION="Bearer {0}".format(self.tok.token))

        map_response = json.loads(response.content)

        self.assertEquals(response.status_code, 400)
        self.assertEquals(map_response["success"], False)
        self.assertEquals(map_response['error'], "Duplicated")

    def test_create_unit_missing_req_field(self):
        data = {
            "title": 'kilograms',
            "types": 2,
        }

        response = self.client.post(self.UNIT_URL, data, format='json',
                                    HTTP_AUTHORIZATION="Bearer {0}".format(self.tok.token))

        map_response = json.loads(response.content)

        self.assertEquals(response.status_code, 400)
        self.assertEquals(map_response["success"], False)
        self.assertEquals(map_response['error'], "Need more data")

    def test_update_unit(self):
        self.unit_category = UnitCategory.objects.create(
            title='weights'
        )
        old_pref = Unit.objects.create(
            title='kilograms',
            types=2,
            ratio=20,
            units_categories=self.unit_category,
            user=self.test_user_system
        )

        update_data = {
            "title": 'grams',
            "types": 2,
            "ratio": 20,
            "units_categories": self.unit_category.id,
        }

        response = self.client.put(self.UNIT_URL_DETAIL.format(old_pref.id),
                                   update_data,
                                   format='json', HTTP_AUTHORIZATION="Bearer {0}".format(self.tok.token))

        map_response = json.loads(response.content)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(map_response["success"], True)
        self.assertEquals(map_response["data"], {
            'title': 'grams',
            'units_categories': self.unit_category.id,
            "types": 2,
            "ratio": 20,
            'delete': False,
            'id': 1,
            'last_modified_users': self.test_user_system.id,
            'user': self.test_user_system.id,
            'last_modified_date': map_response["data"]["last_modified_date"],
        })

    def test_soft_delete_unit(self):
        self.unit_category = UnitCategory.objects.create(
            title='weights'
        )
        old_pref = Unit.objects.create(
            title='kilograms',
            types=2,
            ratio=20,
            units_categories=self.unit_category,
            user=self.test_user_system,
        )

        update_data = {
            "delete": True,
        }

        response = self.client.put(self.UNIT_URL_DETAIL.format(old_pref.id),
                                   update_data,
                                   format='json', HTTP_AUTHORIZATION="Bearer {0}".format(self.tok.token))

        map_response = json.loads(response.content)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(map_response["success"], True)
        self.assertEquals(map_response["data"], {
            'title': 'kilograms',
            'units_categories': self.unit_category.id,
            "types": 2,
            "ratio": 20,
            'delete': True,
            'id': 1,
            'last_modified_users': self.test_user_system.id,
            'user': self.test_user_system.id,
            'last_modified_date': map_response["data"]["last_modified_date"],
        })

    def test_get_unit_list(self):
        self.unit_category = UnitCategory.objects.create(
            title='weights'
        )

        pref1 = Unit.objects.create(
            title='kilograms',
            types=2,
            ratio=20,
            units_categories=self.unit_category,
        )
        pref2 = Unit.objects.create(
            title='grams',
            types=2,
            ratio=40,
            units_categories=self.unit_category,
        )

        response = self.client.get(self.UNIT_URL, format='json',
                                   HTTP_AUTHORIZATION="Bearer {0}".format(self.tok.token))

        self.assertEquals(response.status_code, 200)
        map_response = json.loads(response.content)
        self.assertEquals(len(map_response["data"]), 2)

        self.assertEquals(sorted(map_response["data"][0].keys()), sorted([
            'units_categories', 'types', 'ratio', 'title', 'delete', 'id', 'user', 'last_modified_users',
            'last_modified_date',
        ]))

    def test_get_unit_specific(self):
        self.unit_category = UnitCategory.objects.create(
            title='weights'
        )

        pref = Unit.objects.create(
            title='kilograms',
            types=2,
            ratio=20,
            units_categories=self.unit_category,
            user=self.test_user_system,
            last_modified_users=self.test_user_system
        )

        response = self.client.get(self.UNIT_URL_DETAIL.format(pref.id), format='json',
                                   HTTP_AUTHORIZATION="Bearer {0}".format(self.tok.token))

        map_response = json.loads(response.content)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(map_response["success"], True)
        self.assertEquals(map_response["data"], {
            'title': 'kilograms',
            'units_categories': self.unit_category.id,
            "types": 2,
            "ratio": 20,
            'delete': False,
            'id': 1,
            'last_modified_users': self.test_user_system.id,
            'user': self.test_user_system.id,
            'last_modified_date': map_response["data"]["last_modified_date"],
        })

    def test_delete_unit(self):
        self.unit_category = UnitCategory.objects.create(
            title='weights'
        )

        pref = Unit.objects.create(
            title='kilograms',
            types=2,
            ratio=20,
            units_categories=self.unit_category,
        )

        response = self.client.delete(self.UNIT_URL_DETAIL.format(pref.id), format='json',
                                      HTTP_AUTHORIZATION="Bearer {0}".format(self.tok.token))

        map_response = json.loads(response.content)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(map_response["success"], True)
        self.assertEquals(map_response['message'], "Deleted")
