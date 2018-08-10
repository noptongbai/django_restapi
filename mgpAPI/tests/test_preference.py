# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from datetime import datetime, timedelta
from  common.master_models import Preference
from django.conf import settings
import json


class PreferenceTestCase(APITestCase):
    PREFERENCE_URL = '/api/' + settings.VERSION_API + '/preferences/'
    PREFERENCE_URL_DETAIL = '/api/' + settings.VERSION_API + '/preferences/{}/'

    def setUp(self):
        super(PreferenceTestCase, self).setUp()
        self.test_user = User.objects.create_user('user1', 'a@a.com', 'qwer1234')

    def test_create_preference(self):
        data = {
            "key": "EXPORT_TARGET",
            "value": "8000",
            "description": u"ไฟฟ้าเป้าหมาย"
        }

        self.client.login(username='user1', password='qwer1234')
        response = self.client.post(self.PREFERENCE_URL, data, format='json')

        self.assertEquals(response.status_code, 201)
        self.assertEquals(response.data, {
            'id': 1,
            'created_date': response.data['created_date'],
            'last_modified_date': response.data['last_modified_date'],
            'description': u"ไฟฟ้าเป้าหมาย",
            'key': u'EXPORT_TARGET',
            'value': u"8000",
            'soft_delete': False,
            'created_user': self.test_user.id,
            'last_modified_users': self.test_user.id

        })

    def test_create_preference_missing_req_field(self):
        data = {

        }

        self.client.login(username='user1', password='qwer1234')
        response = self.client.post(self.PREFERENCE_URL, data, format='json')

        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.data, {
            "key": [
                "This field is required."
            ],
            "value": [
                "This field is required."
            ]
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

        self.client.login(username='user1', password='qwer1234')
        response = self.client.post(self.PREFERENCE_URL, data, format='json')

        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.data, {
            "key": [
                "preference with this key already exists."
            ]
        })

    def test_update_preference(self):
        old_pref = Preference.objects.create(
            key='EXPORT_TARGET',
            value='4000',
            description='some desc',
            created_user=self.test_user,
        )

        update_data = {
            "key": "EXPORT_TARGET",
            "value": "8000",
            "description": 'some desc'
        }

        self.client.login(username='user1', password='qwer1234')
        response = self.client.put(self.PREFERENCE_URL_DETAIL.format(old_pref.id),
                                   update_data,
                                   format='json')

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data, {
            'id': old_pref.id,
            'created_date': response.data['created_date'],
            'last_modified_date': response.data['last_modified_date'],
            'description': u"some desc",
            'key': u'EXPORT_TARGET',
            'value': u"8000",
            'soft_delete': False,
            'created_user': self.test_user.id,
            'last_modified_users': self.test_user.id

        })

    def test_soft_delete_preference(self):
        old_pref = Preference.objects.create(
            key='EXPORT_TARGET',
            value='4000',
            description='some desc',
            created_user=self.test_user,
        )

        update_data = {
           "key": "EXPORT_TARGET",
           "value": "4000",
           "soft_delete" : True
        }

        self.client.login(username='user1', password='qwer1234')
        response = self.client.put(self.PREFERENCE_URL_DETAIL.format(old_pref.id),
                                   update_data,
                                   format='json')

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data, {
            'id': old_pref.id,
            'created_date': response.data['created_date'],
            'last_modified_date': response.data['last_modified_date'],
            'description': u"some desc",
            'key': u'EXPORT_TARGET',
            'value': u"4000",
            'soft_delete': True,
            'created_user': self.test_user.id,
            'last_modified_users': self.test_user.id

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

        self.client.login(username='user1', password='qwer1234')
        response = self.client.get(self.PREFERENCE_URL, format='json')

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data["results"]), 2)

        self.assertEquals(sorted(response.data["results"][0].keys()), sorted([
            'value', 'soft_delete', 'id', 'key', 'description', 'created_user','last_modified_users', 'created_date', 'last_modified_date',
        ]))

    def test_get_preference_specific(self):
        pref = Preference.objects.create(
            key='EXPORT_TARGET',
            value='4000',
            description='some desc',
            created_user=self.test_user,
            last_modified_users=self.test_user
        )

        self.client.login(username='user1', password='qwer1234')
        response = self.client.get(self.PREFERENCE_URL_DETAIL.format(pref.id), format='json')

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data, {
            'id': pref.id,
            'created_date': response.data['created_date'],
            'last_modified_date': response.data['last_modified_date'],
            'description': u"some desc",
            'key': u'EXPORT_TARGET',
            'value': u"4000",
            'soft_delete': False,
            'created_user': self.test_user.id,
            'last_modified_users': self.test_user.id

        })

    def test_delete_preference(self):
        pref = Preference.objects.create(
            key='EXPORT_TARGET',
            value='4000',
            description='some desc'
        )

        self.client.login(username='user1', password='qwer1234')
        response = self.client.delete(self.PREFERENCE_URL_DETAIL.format(pref.id), format='json')

        self.assertEquals(response.status_code, 204)

