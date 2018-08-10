from transactions.models import InputDetail, WithdrawDetail
from mgpAPI.services.transaction_log import transaction_log_create
from  products.models import Product
from  rest_framework import serializers


def withdraw_stock_after_synced():
    print "start fifo"
    withdraw_instances = WithdrawDetail.objects.filter(erp_type=True, used=False,
                                                       ).order_by(
        'created_date', 'id')
    total = withdraw_instances.count()
    count = 1
    for withdraw in withdraw_instances:
        print str(count) + ' / ' + str(total)
        input_instances = InputDetail.objects.filter(erp_type=True, product=withdraw.product,
                                                     left_quantity__gt=0).order_by(
            'created_date', 'id')

        need_quantity = float(withdraw.quantity)
        for input in input_instances:

            if need_quantity != 0:
                if need_quantity > input.left_quantity:
                    need_quantity = need_quantity - input.left_quantity
                    input.left_quantity = 0
                    input.reserve_quantity = input.left_quantity
                    input.save()
                elif need_quantity == input.left_quantity:
                    input.left_quantity = 0
                    input.reserve_quantity = input.left_quantity
                    input.save()
                    break
                else:
                    input.left_quantity = input.left_quantity - need_quantity
                    input.reserve_quantity = input.left_quantity
                    input.save()
                    break
            else:
                break
        withdraw.used = True
        withdraw.save()
        count = count + 1
