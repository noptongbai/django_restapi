# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from datetime import datetime, timedelta
from transactions.models import Transaction, InputDetail
from mgpAPI.erp_services.syn_all import syncall
from mgpAPI.erp_services.po_rcpt_sync import purchase_order_rcpt_sync, purchase_order_rcpt_line_sync
from mgpAPI.erp_services.po_sync import purchase_order_sync, purchase_order_line_sync
from products.models import Product
from units.models import Unit, UnitCategory
from common.master_models import Supplier, Sector
from django.conf import settings
import json


class InputTransactionTestCase(APITestCase):
    INPUT_URL = '/api/' + settings.VERSION_API + '/transactions/input/'
    WITHDRAW_URL = '/api/' + settings.VERSION_API + '/transactions/withdraw/'
    SCRAP_URL = '/api/' + settings.VERSION_API + '/transactions/scrap/'
    ADJUST_URL = '/api/' + settings.VERSION_API + '/transactions/adjust/'
    RETURN_URL = '/api/' + settings.VERSION_API + '/transactions/return/'

    def setUp(self):
        super(InputTransactionTestCase, self).setUp()
        self.test_user = User.objects.create_user('user1', 'a@a.com', 'qwer1234')
        syncall()

    def test_create_input_transaction(self):
        data = {
            "date": "2017-05-25T21:54:49.802002",
            "input_lines": [
                {"uom": 1, "product": 1, "quantity": 100, "humidity": 0,
                 "supplier": 1, "truck_license": "กท123",
                 "unit_price": 30}

            ]
        }
        self.client.login(username='user1', password='qwer1234')
        product_get = Product.objects.get(id=1)
        response = self.client.post(self.INPUT_URL, data, format='json')
        self.assertEquals(response.status_code, 201)
        self.assertEquals(Product.objects.get(id=1).quantity, 100 + product_get.quantity)
        self.assertEquals(Product.objects.get(id=1).valuation, 100 * 30 + product_get.valuation)

    def test_create_withdraw_transaction(self):
        data = {
            "date": "2017-12-17T22:08:37.838Z",
            "withdraw_lines": [
                {"uom": 1, "product": 2, "quantity": 50, "humidity": 0,
                 "supplier": 1, "sector": 1}

            ]
        }
        self.client.login(username='user1', password='qwer1234')
        product_get = Product.objects.get(id=2)
        response = self.client.post(self.WITHDRAW_URL, data, format='json')
        self.assertEquals(response.status_code, 201)
        input1 = InputDetail.objects.get(id=43)
        input2 = InputDetail.objects.get(id=17)
        input3 = InputDetail.objects.get(id=18)
        self.assertEquals(Product.objects.get(id=2).quantity, product_get.quantity - 288.54)
        self.assertEquals(Product.objects.get(id=2).valuation,
                          product_get.valuation - response.data["withdraw_lines"][0]["amount"])
        self.assertEquals(input1.left_quantity, 0)
        self.assertEquals(input2.left_quantity, 0)
        self.assertEquals(input3.left_quantity, 0)
        self.assertEquals(int(response.data["withdraw_lines"][0]["unit_price"]),
                          int(((1080.0 * 168.54) + (1080 * 60) + (1050 * 60)) / 288.54))

    def test_create_scrap_transaction(self):
        data = {
            "date": "2017-05-25T21:54:49.802002",
            "scrap_lines": [
                {"uom": 1, "product": 2, "quantity": 288.54, "humidity": 0,
                 "supplier": 1, "sector": 1}

            ]
        }
        self.client.login(username='user1', password='qwer1234')
        product_get = Product.objects.get(id=2)
        response = self.client.post(self.SCRAP_URL, data, format='json')
        self.assertEquals(response.status_code, 201)
        input1 = InputDetail.objects.get(id=43)
        input2 = InputDetail.objects.get(id=17)
        input3 = InputDetail.objects.get(id=18)
        self.assertEquals(Product.objects.get(id=2).quantity, product_get.quantity - 288.54)
        self.assertEquals(Product.objects.get(id=2).valuation,
                          product_get.valuation - response.data["scrap_lines"][0]["amount"])
        self.assertEquals(input1.left_quantity, 0)
        self.assertEquals(input2.left_quantity, 0)
        self.assertEquals(input3.left_quantity, 0)
        self.assertEquals(int(response.data["scrap_lines"][0]["unit_price"]),
                          int(((1080.0 * 168.54) + (1080 * 60) + (1050 * 60)) / 288.54))

    def test_create_return_transaction(self):
        data = {
            "date": "2017-05-25T21:54:49.802002",
            "return_lines": [
                {"uom": 1, "product": 2, "quantity": 288.54, "humidity": 0,
                 "supplier": 1, "sector": 1}

            ]
        }
        self.client.login(username='user1', password='qwer1234')
        product_get = Product.objects.get(id=2)
        response = self.client.post(self.RETURN_URL, data, format='json')
        self.assertEquals(response.status_code, 201)
        input1 = InputDetail.objects.get(id=43)
        input2 = InputDetail.objects.get(id=17)
        input3 = InputDetail.objects.get(id=18)
        self.assertEquals(Product.objects.get(id=2).quantity, product_get.quantity - 288.54)
        self.assertEquals(Product.objects.get(id=2).valuation,
                          product_get.valuation - response.data["return_lines"][0]["amount"])
        self.assertEquals(input1.left_quantity, 0)
        self.assertEquals(input2.left_quantity, 0)
        self.assertEquals(input3.left_quantity, 0)
        self.assertEquals(int(response.data["return_lines"][0]["unit_price"]),
                          int(((1080.0 * 168.54) + (1080 * 60) + (1050 * 60)) / 288.54))

    def test_create_adjust_withdraw_transaction(self):
        data = {
            "date": "2017-05-25T21:54:49.802002",
            "adjust_lines": [
                {"uom": 1, "product": 2, "quantity": -288.54, "humidity": 0,
                 "supplier": 1, "sector": 1}

            ]
        }
        self.client.login(username='user1', password='qwer1234')
        product_get = Product.objects.get(id=2)
        response = self.client.post(self.ADJUST_URL, data, format='json')
        self.assertEquals(response.status_code, 201)
        input1 = InputDetail.objects.get(id=43)
        input2 = InputDetail.objects.get(id=17)
        input3 = InputDetail.objects.get(id=18)
        self.assertEquals(Product.objects.get(id=2).quantity, product_get.quantity - 288.54)
        self.assertEquals(Product.objects.get(id=2).valuation,
                          product_get.valuation - response.data["adjust_lines"][0]["amount"])
        self.assertEquals(input1.left_quantity, 0)
        self.assertEquals(input2.left_quantity, 0)
        self.assertEquals(input3.left_quantity, 0)
        self.assertEquals(int(response.data["adjust_lines"][0]["unit_price"]),
                          int(((1080.0 * 168.54) + (1080 * 60) + (1050 * 60)) / 288.54))

    def test_create_scrap_withdraw_notfifo(self):
        data = {
            "date": "2017-05-25T21:54:49.802002",
            "scrap_lines": [
                {"uom": 38, "product": 2, "sector": 1, "array": [{"id": 17, "qut": 60}, {"id": 18, "qut": 60}]}

            ]

        }
        self.client.login(username='user1', password='qwer1234')
        product_get = Product.objects.get(id=2)
        response = self.client.post(self.SCRAP_URL, data, format='json')
        self.assertEquals(response.status_code, 201)
        input1 = InputDetail.objects.get(id=17)
        input2 = InputDetail.objects.get(id=18)
        self.assertEquals(Product.objects.get(id=2).quantity, product_get.quantity - 120)
        self.assertEquals(Product.objects.get(id=2).valuation,
                          product_get.valuation - (1080*60)-(1050*60))
        self.assertEquals(input1.left_quantity, 0)
        self.assertEquals(input2.left_quantity, 0)
        self.assertEquals(int(response.data["scrap_lines"][0]["unit_price"]),
                          int(((1080.0 * 60) + (1050 * 60)) / 120))

    def test_create_return_withdraw_notfifo(self):
        data = {
            "date": "2017-05-25T21:54:49.802002",
            "return_lines": [
                {"uom": 38, "product": 2, "sector": 1, "array": [{"id": 17, "qut": 60}, {"id": 18, "qut": 60}]}

            ]

        }
        self.client.login(username='user1', password='qwer1234')
        product_get = Product.objects.get(id=2)
        response = self.client.post(self.RETURN_URL, data, format='json')
        self.assertEquals(response.status_code, 201)
        input1 = InputDetail.objects.get(id=17)
        input2 = InputDetail.objects.get(id=18)
        self.assertEquals(Product.objects.get(id=2).quantity, product_get.quantity - 120)
        self.assertEquals(Product.objects.get(id=2).valuation,
                          product_get.valuation - (1080 * 60) - (1050 * 60))
        self.assertEquals(input1.left_quantity, 0)
        self.assertEquals(input2.left_quantity, 0)
        self.assertEquals(int(response.data["return_lines"][0]["unit_price"]),
                          int(((1080.0 * 60) + (1050 * 60)) / 120))

    def test_create_adjust_withdraw_notfifo(self):
        data = {
            "date": "2017-05-25T21:54:49.802002",
            "adjust_lines": [
                {"uom": 38, "product": 2, "sector": 1, "array": [{"id": 17, "qut": 60}, {"id": 18, "qut": 60}]}

            ]

        }
        self.client.login(username='user1', password='qwer1234')
        product_get = Product.objects.get(id=2)
        response = self.client.post(self.ADJUST_URL, data, format='json')
        self.assertEquals(response.status_code, 201)
        input1 = InputDetail.objects.get(id=17)
        input2 = InputDetail.objects.get(id=18)
        self.assertEquals(Product.objects.get(id=2).quantity, product_get.quantity - 120)
        self.assertEquals(Product.objects.get(id=2).valuation,
                          product_get.valuation - (1080 * 60) - (1050 * 60))
        self.assertEquals(input1.left_quantity, 0)
        self.assertEquals(input2.left_quantity, 0)
        self.assertEquals(int(response.data["adjust_lines"][0]["unit_price"]),
                          int(((1080.0 * 60) + (1050 * 60)) / 120))

    def test_create_adjust_input_transaction(self):
        data = {
            "date": "2017-05-25T21:54:49.802002",
            "adjust_lines": [
                {"uom": 38, "product": 1, "sector": 1, "quantity": 20, "unit_price": 30}

            ]

        }
        self.client.login(username='user1', password='qwer1234')
        product_get = Product.objects.get(id=1)
        response = self.client.post(self.ADJUST_URL, data, format='json')
        self.assertEquals(response.status_code, 201)
        self.assertEquals(Product.objects.get(id=1).quantity, 20 + product_get.quantity)
        self.assertEquals(Product.objects.get(id=1).valuation, 20 * 30 + product_get.valuation)
