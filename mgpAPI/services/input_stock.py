from mgpAPI.services.convert_humidity import convert_humidity
from products.models import Product
from transactions.models import UnitCostHistory, TransactionLog
from mgpAPI.erp_services.jounal_to_erp import transaction_log_sync


def input_stock(data, input_instance):
    if data.get("humidity") != None:
        convert_humidity_value = convert_humidity(data["humidity"], data["quantity"])
    else:
        convert_humidity_value = data["quantity"]

    input_instance.left_quantity = data["quantity"]
    input_instance.unit_price = data["unit_price"]
    input_instance.humidity_converted = convert_humidity_value
    input_instance.amount = data["unit_price"] * data["quantity"]
    input_instance.save()

    product_instance = Product.objects.get(id=data["product"].id)
    product_instance.save()
    try:
        transaction_obj = TransactionLog.objects.order_by('-last_modified_date')[0]
        line_number = transaction_obj.lines + 10000
    except Exception:
        line_number = 10000
    TransactionLog.objects.create(product=product_instance, uom=product_instance.uom, name="input_stock",
                                  unit_price=data["unit_price"],
                                  input_transaction=input_instance, quantity=data["quantity"], lines=line_number)

    # transaction_log_sync()


def update_stock(data, input_instance):
    if (input_instance.humidity != data["humidity"] or input_instance.product != data[
        "product"] or input_instance.unit_price != data["unit_price"] or input_instance.quantity != data["quantity"]):

        product_instance = Product.objects.get(id=input_instance.product.id)
        product_instance.quantity = product_instance.quantity - input_instance.left_quantity
        product_instance.save()

        if data.get("humidity") != None:
            convert_humidity_value = convert_humidity(data["humidity"], data["quantity"])
        else:
            convert_humidity_value = data["quantity"]

        product_instance = data["product"]
        product_instance.quantity = product_instance.quantity + convert_humidity_value
        product_instance.save()

        input_instance.left_quantity = convert_humidity_value
        input_instance.humidity = data["humidity"]
        input_instance.unit_price = data["cost"] / (convert_humidity_value)
        input_instance.quantity = data["quantity"]
        input_instance.cost = data["cost"]
        input_instance.product = product_instance
        input_instance.save()

        log_transaction = TransactionLog.objects.get(input_transaction=input_instance)
        log_transaction.quantity = convert_humidity_value
        log_transaction.product = product_instance
        log_transaction.unit = product_instance.unit
        log_transaction.save()
