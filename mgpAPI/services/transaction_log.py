from  transactions.models import TransactionLog
from  mgpAPI.erp_services.jounal_to_erp import transaction_log_sync
import sys


def transaction_log_create(withdraw_instance, product_instance, uom_instance, type, quantity, unit_price):
    try:
        transaction_obj = TransactionLog.objects.order_by('-last_modified_date')[0]
        line_number = transaction_obj.lines + 10000
    except Exception:
        line_number = 50000

    if type == 1:
        TransactionLog.objects.create(withdraw_transaction=withdraw_instance, product=product_instance,
                                      uom=uom_instance,
                                      quantity=-quantity, unit_price=unit_price, lines=line_number)

    elif type == 2:
        TransactionLog.objects.create(scrap_transaction=withdraw_instance, product=product_instance,
                                      uom=uom_instance,
                                      quantity=-quantity, unit_price=unit_price, lines=line_number)

    elif type == 3:
        TransactionLog.objects.create(return_transaction=withdraw_instance, product=product_instance,
                                      uom=uom_instance,
                                      quantity=-quantity, unit_price=unit_price, lines=line_number)

    elif type == 4:
        TransactionLog.objects.create(adjust_transaction=withdraw_instance, product=product_instance,
                                      uom=uom_instance,
                                      quantity=-quantity, unit_price=unit_price, lines=line_number)
