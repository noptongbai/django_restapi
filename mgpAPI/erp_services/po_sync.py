from  mgpAPI.erp_services.conncet_database import initconncetion
from  purchase_orders.models import PurchaseOrder, PurchaseOrderLine
from  common.master_models import Supplier
from  products.models import Product
import binascii


def purchase_order_sync():
    cnxn = initconncetion()
    cursor = cnxn.cursor()

    try:
        purchase_order = PurchaseOrder.objects.all().order_by('-timestamp')[0]
        timestamp = str(purchase_order.timestamp)
    except Exception as e:
        timestamp = str(0)

    cursor.execute('SELECT PO."timestamp",PO."No_",PO."Buy-from Vendor No_",PO."Posting Date" '
                   'FROM "Mahachai Green co_,Ltd$Purchase Header" As PO INNER JOIN "Mahachai Green co_,Ltd$Purchase Line" '
                   'As PL ON PL."Document No_" = PO."No_" Where PL."Type" = 2 AND CAST(PO."timestamp" as int) >' + timestamp + ' GROUP By PO."No_",PO."timestamp",PO."Buy-from Vendor No_",PO."Posting Date"')

    row = cursor.fetchone()
    while row:
        try:
            if len(Supplier.objects.filter(ext_code=str(row[2].encode('utf-8').strip()))) == 1:
                supplier = Supplier.objects.get(ext_code=str(row[2].encode('utf-8').strip()))
            else:
                supplier = None
            purchase_order = PurchaseOrder.objects.get(ext_code=str(row[1].encode('utf-8').strip()))
            hex2 = '0x' + str(binascii.b2a_hex(row[0]))
            time = int(hex2, 16)
            purchase_order.timestamp = time
            purchase_order.supplier = supplier
            purchase_order.posting_date = str(row[3].encode('utf-8').strip())
            purchase_order.save()
        except Exception as a:
            if len(Supplier.objects.filter(ext_code=str(row[2].encode('utf-8').strip()))) == 1:
                supplier = Supplier.objects.get(ext_code=str(row[2].encode('utf-8').strip()))
            else:
                supplier = None

            hex2 = '0x' + str(binascii.b2a_hex(row[0]))
            time = int(hex2, 16)
            PurchaseOrder.objects.create(timestamp=time, po=str(row[1].encode('utf-8').strip()),
                                         posting_date=row[3], supplier=supplier
                                         )
        row = cursor.fetchone()


def purchase_order_line_sync():
    cnxn = initconncetion()
    cursor = cnxn.cursor()

    try:
        purchase_order_line = PurchaseOrderLine.objects.all().order_by('-timestamp')[0]
        timestamp = str(purchase_order_line.timestamp)
    except Exception as e:
        timestamp = str(0)

    cursor.execute(
        'SELECT "timestamp","Document No_","Line No_","Buy-from Vendor No_","No_","Quantity",'
        '"Outstanding Quantity","Direct Unit Cost","Description" FROM "Mahachai Green co_,Ltd$Purchase Line"'
        'Where  Type=2 AND CAST(timestamp as int) >' + timestamp)
    row = cursor.fetchone()
    while row:
        try:
            purchase_order_instance = PurchaseOrder.objects.filter(po=str(row[1].encode('utf-8').strip()))[0]
            purchase_order_line_instance = PurchaseOrderLine.objects.get(purchase_orders=purchase_order_instance,
                                                                         line_no=str(row[2].encode('utf-8').strip()))
            if len(Supplier.objects.filter(ext_code=str(row[3].encode('utf-8').strip()))) == 1:
                supplier = Supplier.objects.get(ext_code=str(row[3].encode('utf-8').strip()))
            else:
                supplier = None
            if len(Product.objects.filter(ext_code=str(row[4].encode('utf-8').strip()))) == 1:
                product = Product.objects.get(ext_code=str(row[4].encode('utf-8').strip()))
                uom = product.uom
            else:
                product = None
                uom = None

            if row[5] == row[6]:
                status = 0
            elif row[6] == 0:
                status = 2
            else:
                status = 1

            hex2 = '0x' + str(binascii.b2a_hex(row[0]))
            time = int(hex2, 16)
            purchase_order_line_instance.timestamp = time
            purchase_order_line_instance.supplier = supplier
            purchase_order_line_instance.products = product
            purchase_order_line_instance.uom = uom
            purchase_order_line_instance.quantity = row[5]
            purchase_order_line_instance.outstanding_quantity = row[6]
            purchase_order_line_instance.unit_cost = row[7]
            purchase_order_line_instance.description = str(row[8].encode('utf-8').strip())
            purchase_order_line_instance.delivered = status
            purchase_order_line_instance.save()
        except Exception as e:
            purchase_order_instance = PurchaseOrder.objects.filter(po=str(row[1].encode('utf-8').strip()))[0]
            if len(Supplier.objects.filter(ext_code=str(row[3].encode('utf-8').strip()))) == 1:
                supplier = Supplier.objects.get(ext_code=str(row[3].encode('utf-8').strip()))
            else:
                supplier = None
            if len(Product.objects.filter(ext_code=str(row[4].encode('utf-8').strip()))) == 1:
                product = Product.objects.get(ext_code=str(row[4].encode('utf-8').strip()))
                uom = product.uom
            else:
                product = None
                uom = None

            if row[5] == row[6]:
                status = 0
            elif row[6] == 0:
                status = 2
            else:
                status = 1

            hex2 = '0x' + str(binascii.b2a_hex(row[0]))
            time = int(hex2, 16)
            PurchaseOrderLine.objects.create(timestamp=time, supplier=supplier, product=product, uom=uom,
                                             quantity=row[5],
                                             outstanding_quantity=row[6],
                                             unit_cost=row[7],
                                             purchase_orders=purchase_order_instance, line_no=str(row[2]),
                                             description=str(row[8].encode('utf-8').strip()),delivered=status
                                             )

        row = cursor.fetchone()
