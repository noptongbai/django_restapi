from  products.models import Product
from  transactions.models import Transaction, TransactionLog, InputDetail
from  mgpAPI.services.input_to_juntion import input_juntion
from mgpAPI.services.transaction_log import transaction_log_create
from  rest_framework import serializers


def withdraw_stock_withoutfifo(data, withdraw_instance, type, array):
    product_instance = Product.objects.get(id=data["product"].id)

    for input_data in array:
        input = InputDetail.objects.get(id=input_data.get('id'))
        if input.left_quantity < input_data.get('qut'):
            raise serializers.ValidationError({"error": "not enough in stock"})
        if input.product != product_instance:
            raise serializers.ValidationError({"error": "not same product"})

    i = 0
    for input_data in array:
        input = InputDetail.objects.get(id=input_data.get('id'))
        qut = input_data.get('qut')
        input.left_quantity = input.left_quantity - qut
        input.used = True
        input.save()

        if (i == 0):
            withdraw_instance.unit_price = input.unit_price
            withdraw_instance.amount = input.unit_price * qut
            withdraw_instance.quantity = qut
            withdraw_instance.save()

        else:
            unit_price_fifo = ((withdraw_instance.unit_price * withdraw_instance.quantity) + (
                input.unit_price * qut)) / (withdraw_instance.quantity + qut)
            withdraw_instance.unit_price = unit_price_fifo
            withdraw_instance.amount = unit_price_fifo * (withdraw_instance.quantity + qut)
            withdraw_instance.quantity = withdraw_instance.quantity + qut
            withdraw_instance.save()

        input_juntion(input, withdraw_instance, type, qut, input.created_date, input.note,
                      input.supplier)
        i = i + 1

    product_instance.quantity = product_instance.quantity - withdraw_instance.quantity
    product_instance.valuation = product_instance.valuation - withdraw_instance.amount
    product_instance.save()

    transaction_log_create(withdraw_instance, product_instance, product_instance.uom, type, withdraw_instance.quantity,
                           withdraw_instance.unit_price)
