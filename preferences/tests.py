# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from  users.models import UserSystem, UserCategory
from oauth2_provider.models import Application, AccessToken
from rest_framework.test import APITestCase
from datetime import datetime, timedelta
from preferences.models import Preference
from django.conf import settings
import json


class PreferenceTestCase(APITestCase):
    PREFERENCE_URL = '/api/'+ settings.VERSION_API + '/preferences/'
    PREFERENCE_URL_DETAIL =  '/api/'+ settings.VERSION_API + '/preferences/?id={}'
    maxDiff = None

    def setUp(self):
        super(PreferenceTestCase, self).setUp()
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

    def test_create_preference(self):
        data = {
            "key": "EXPORT_TARGET",
            "value": "8000",
            "description": u"ไฟฟ้าเป้าหมาย",

        }

        response = self.client.post(self.PREFERENCE_URL, data, format='json',
                                    HTTP_AUTHORIZATION="Bearer {0}".format(self.tok.token))

        map_response = json.loads(response.content)

        self.assertEquals(response.status_code, 201)

        self.assertEquals(map_response["data"], {
            'value': 8000.0,
            'delete': False,
            'id': 1,
            'key': u'EXPORT_TARGET',
            'description': u"ไฟฟ้าเป้าหมาย",
            'last_modified_users': self.test_user_system.id,
            'user': self.test_user_system.id,
            'last_modified_date': map_response["data"]["last_modified_date"],
        })

    def test_create_preference_without_authenticate(self):
        data = {
            "key": "EXPORT_TARGET",
            "value": "8000",
            "description": u"ไฟฟ้าเป้าหมาย"
        }

        response = self.client.post(self.PREFERENCE_URL, data, format='json')

        self.assertEquals(response.status_code, 401)

    def test_create_preference_duplicated(self):
        pref = Preference.objects.create(
            key='EXPORT_TARGET',
            value='4000',
            description='some desc'
        )

        data = {
            "key": "EXPORT_TARGET",
            "value": "8000",
            "description": u"ไฟฟ้าเป้าหมาย"
        }
        response = self.client.post(self.PREFERENCE_URL, data, format='json',
                                    HTTP_AUTHORIZATION="Bearer {0}".format(self.tok.token))

        map_response = json.loads(response.content)

        self.assertEquals(response.status_code, 400)
        self.assertEquals(map_response["success"], False)
        self.assertEquals(map_response['error'], "Duplicated")

    def test_create_preference_missing_req_field(self):
        data = {
            "value": "8000",
            "description": u"ไฟฟ้าเป้าหมาย"
        }

        response = self.client.post(self.PREFERENCE_URL, data, format='json',
                                    HTTP_AUTHORIZATION="Bearer {0}".format(self.tok.token))

        map_response = json.loads(response.content)

        self.assertEquals(response.status_code, 400)
        self.assertEquals(map_response["success"], False)
        self.assertEquals(map_response['error'], "Not found key or value or description")

    def test_update_preference(self):
        old_pref = Preference.objects.create(
            key='EXPORT_TARGET',
            value='4000',
            description='some desc',
            user=self.test_user_system,
        )

        update_data = {
            "key": "EXPORT_TARGET",
            "value": "8000",
            "description": 'some desc'
        }

        response = self.client.put(self.PREFERENCE_URL_DETAIL.format(old_pref.id),
                                   update_data,
                                   format='json', HTTP_AUTHORIZATION="Bearer {0}".format(self.tok.token))

        map_response = json.loads(response.content)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(map_response["success"], True)
        self.assertEquals(map_response["data"], {
            'value': 8000.0,
            'delete': False,
            'id': old_pref.id,
            'key': u'EXPORT_TARGET',
            'description': 'some desc',
            'last_modified_users': self.test_user_system.id,
            'user': self.test_user_system.id,
            'last_modified_date': map_response["data"]["last_modified_date"],
        })

    def test_soft_delete_preference(self):
        old_pref = Preference.objects.create(
            key='EXPORT_TARGET',
            value='4000',
            description='some desc',
            user=self.test_user_system
        )

        update_data = {
            "delete": True,
        }

        response = self.client.put(self.PREFERENCE_URL_DETAIL.format(old_pref.id),
                                   update_data,
                                   format='json', HTTP_AUTHORIZATION="Bearer {0}".format(self.tok.token))

        map_response = json.loads(response.content)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(map_response["success"], True)
        self.assertEquals(map_response["data"], {
            'value': 4000.0,
            'delete': True,
            'id': old_pref.id,
            'key': u'EXPORT_TARGET',
            'description': 'some desc',
            'last_modified_users': self.test_user_system.id,
            'user': self.test_user_system.id,
            'last_modified_date': map_response["data"]["last_modified_date"],
        })

    def test_get_preference_list(self):
        pref1 = Preference.objects.create(
            key='EXPORT_TARGET',
            value='4000',
            description='some desc'
        )
        pref2 = Preference.objects.create(
            key='OUTAGE_LIMIT',
            value='200',
            description='some desc'
        )

        response = self.client.get(self.PREFERENCE_URL, format='json',
                                   HTTP_AUTHORIZATION="Bearer {0}".format(self.tok.token))

        self.assertEquals(response.status_code, 200)
        map_response = json.loads(response.content)
        self.assertEquals(len(map_response["data"]), 2)

        self.assertEquals(sorted(map_response["data"][0].keys()), sorted([
            'value', 'delete', 'id', 'key', 'description', 'user', 'last_modified_users', 'last_modified_date',
        ]))

    def test_get_preference_specific(self):
        pref = Preference.objects.create(
            key='EXPORT_TARGET',
            value='4000',
            description='some desc',
            user=self.test_user_system,
            last_modified_users=self.test_user_system
        )

        response = self.client.get(self.PREFERENCE_URL_DETAIL.format(pref.id), format='json',
                                   HTTP_AUTHORIZATION="Bearer {0}".format(self.tok.token))

        map_response = json.loads(response.content)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(map_response["success"], True)
        self.assertEquals(map_response["data"], {
            'value': 4000.0,
            'delete': False,
            'id': pref.id,
            'key': u'EXPORT_TARGET',
            'description': 'some desc',
            'last_modified_users': self.test_user_system.id,
            'user': self.test_user_system.id,
            'last_modified_date': map_response["data"]["last_modified_date"],
        })

    def test_delete_preference(self):
        pref = Preference.objects.create(
            key='EXPORT_TARGET',
            value='4000',
            description='some desc'
        )

        response = self.client.delete(self.PREFERENCE_URL_DETAIL.format(pref.id), format='json',
                                      HTTP_AUTHORIZATION="Bearer {0}".format(self.tok.token))

        map_response = json.loads(response.content)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(map_response["success"], True)
        self.assertEquals(map_response['message'], "Deleted")
