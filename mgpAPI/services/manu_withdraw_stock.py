from transactions.models import InputDetail, TransactionLog
from mgpAPI.services.transaction_log import transaction_log_create
from  products.models import Product
from  rest_framework import serializers
from  mgpAPI.services.input_to_juntion import input_juntion
from django.db.models import Sum

def manu_withdraw_stock(data, withdraw_instance, manu_instance, type):
    product_instance = Product.objects.get(id=data["product"].id)
    quantity = data["quantity"]

    quantity_left_front = InputDetail.objects.filter(product=product_instance).aggregate(Sum('reserve_quantity'))
    if quantity_left_front >= quantity:

        input_instances = InputDetail.objects.filter(product=product_instance, reserve_quantity__gt=0, erp_type=True,
                                                     left_quantity__gt=0).order_by(
            'created_date', 'id')
        need_quantity = quantity
        current_quantity = 0
        unit_cost_fifo = 0

        for input_instance in input_instances:

            if current_quantity == 0:
                unit_cost_fifo = input_instance.unit_price

                if need_quantity <= input_instance.reserve_quantity:
                    input_instance.reserve_quantity = input_instance.reserve_quantity - need_quantity
                    input_instance.save()

                    withdraw_instance.unit_price = input_instance.unit_price
                    withdraw_instance.amount = input_instance.unit_price * need_quantity
                    withdraw_instance.save()

                    input_juntion(input_instance, withdraw_instance, type, need_quantity, input_instance.created_date,
                                  input_instance.note, input_instance.supplier)

                    transaction_log_create(withdraw_instance, product_instance, product_instance.uom, type, quantity,
                                           withdraw_instance.unit_price)
                    break;
                else:
                    current_quantity = input_instance.reserve_quantity
                    need_quantity = need_quantity - input_instance.reserve_quantity

                    input_instance.reserve_quantity = 0
                    input_instance.save()

                    input_juntion(input_instance, withdraw_instance, type, current_quantity,
                                  input_instance.created_date, input_instance.note, input_instance.supplier)



            else:

                if need_quantity <= input_instance.reserve_quantity:

                    input_instance.reserve_quantity = input_instance.reserve_quantity - need_quantity
                    input_instance.save()

                    current_cost = current_quantity * unit_cost_fifo
                    cost_cal = need_quantity * input_instance.unit_price
                    unit_cost_fifo = (cost_cal + current_cost) / (current_quantity + need_quantity)

                    withdraw_instance.unit_price = unit_cost_fifo
                    withdraw_instance.amount = unit_cost_fifo * (current_quantity + need_quantity)
                    withdraw_instance.save()

                    input_juntion(input_instance, withdraw_instance, type, need_quantity, input_instance.created_date,
                                  input_instance.note, input_instance.supplier)

                    transaction_log_create(withdraw_instance, product_instance, product_instance.uom, type, quantity,
                                           withdraw_instance.unit_price)
                    break;

                else:
                    used_quantity = input_instance.reserve_quantity
                    current_cost = current_quantity * unit_cost_fifo
                    cost_cal = input_instance.reserve_quantity * input_instance.unit_price
                    unit_cost_fifo = (cost_cal + current_cost) / (current_quantity + input_instance.reserve_quantity)

                    current_quantity = current_quantity + input_instance.reserve_quantity
                    need_quantity = need_quantity - input_instance.reserve_quantity

                    input_instance.reserve_quantity = 0
                    input_instance.save()

                    input_juntion(input_instance, withdraw_instance, type, used_quantity, input_instance.created_date,
                                  input_instance.note, input_instance.supplier)

    else:
        withdraw_instance.quantity = 0
        withdraw_instance.save()
        manu_instance.quantity = 0
        manu_instance.save()
        raise serializers.ValidationError({"error": "not enough in stock"})
