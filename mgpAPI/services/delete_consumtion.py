from transactions.models import InputDetail, Transaction
from mgpAPI.services.input_stock import input_stock
from datetime import datetime


def delete_consumtion(withdraw, user, product, uom, quantity):
    transaction = Transaction.objects.create(types=0, created_user=user,
                                             last_modified_users=user,
                                             date=datetime.now())

    track_data = {}
    track_data["product"] = product
    track_data["quantity"] = quantity
    track_data["uom"] = uom
    track_data["unit_price"] = withdraw.unit_price

    input_instance = InputDetail.objects.create(transaction=transaction,
                                                created_user=user,
                                                last_modified_users=user,
                                                **track_data)

    if input_instance != None:
        input_stock(track_data, input_instance)
