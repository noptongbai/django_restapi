from mgpAPI.services.convert_humidity import convert_humidity
from  products.models import Product
from  transactions.models import InputDetail, TransactionLog, Transaction
from mgpAPI.services.transaction_log import transaction_log_create


def adjust_input_stock(data, adjust_instance, user, date):
    if data.get("humidity") != None:
        convert_humidity_value = convert_humidity(data["humidity"], data["quantity"])
        humidity = data["humidity"]
    else:
        convert_humidity_value = data["quantity"]
        humidity = 0

    product_instance = Product.objects.get(id=data["product"].id)
    product_instance.save()

    transaction = Transaction.objects.create(types=0, created_user=user,
                                             last_modified_users=user, date=date)

    InputDetail.objects.create(transaction=transaction, quantity=convert_humidity_value, left_quantity=data["quantity"],
                               humidity_converted=convert_humidity_value,
                               product=product_instance, uom=data["uom"], unit_price=data["unit_price"],
                               amount=data["unit_price"] * data["quantity"], humidity=
                               humidity, created_user=user,
                               last_modified_users=user)

    transaction_log_create(adjust_instance, product_instance, product_instance.uom, 4, adjust_instance.quantity,
                           adjust_instance.unit_price)


def update_adjust_stock(data, adjust_instance):
    if (adjust_instance.product != data[
        "product"] or adjust_instance.unit != data[
        "unit"] or adjust_instance.quantity != data["quantity"]):
        product_instance = Product.objects.get(id=adjust_instance.product.id)
        product_instance.quantity = product_instance.quantity - adjust_instance.base_unit_quantity
        product_instance.save()

        input_instance = InputDetail.objects.get(id=data["input_transaction"].id)
        input_instance.left_quantity = input_instance.left_quantity - adjust_instance.base_unit_quantity
        input_instance.quantity = input_instance.quantity - adjust_instance.base_unit_quantity
        input_instance.save()

        unit_instance = data["unit"]
        product_instance = Product.objects.get(id=data["product"].id)
        number = convert_by_type(unit_instance.type, unit_instance.ratio)
        base_unit_quantity = data["quantity"] * number

        product_instance.quantity = product_instance.quantity + base_unit_quantity
        product_instance.save()

        input_instance.left_quantity = input_instance.left_quantity + base_unit_quantity
        input_instance.quantity = input_instance.quantity + base_unit_quantity
        input_instance.save()

        log_transaction = TransactionLog.objects.get(adjust_transaction=adjust_instance)
        log_transaction.product = product_instance
        log_transaction.unit = product_instance.unit
        log_transaction.quantity = base_unit_quantity
        log_transaction.save()
