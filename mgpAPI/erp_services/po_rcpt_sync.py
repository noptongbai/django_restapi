from  transactions.models import Transaction, InputDetail, WithdrawDetail
from  mgpAPI.erp_services.conncet_database import initconncetion
from  common.master_models import Supplier
from  products.models import Product
import binascii, decimal
from  mgpAPI.services.withdraw_stock_synced import withdraw_stock_after_synced


def purchase_order_rcpt_line_sync():
    print  "start call I and W"
    cnxn = initconncetion()
    cursor = cnxn.cursor()

    try:
        transaction_line = Transaction.objects.filter(erp_type=True).order_by('-timestamp')[0]
        timestamp = str(transaction_line.timestamp)
        erp_no = str(transaction_line.erp_no)
        print erp_no
        print timestamp
    except Exception as e:
        erp_no = 0
        timestamp = str(0)

    cursor.execute(
        'SELECT T1."timestamp",T1."Item No_",T1."Posting Date",T1."Document No_",T1."Quantity",T1."Cost Amount (Stock)",T2."Unit Cost",T1."Source No_",T1."Entry No_" '
        'FROM "Mahachai Green co_,Ltd$Item Ledger Entry" As T1 LEFT JOIN  "Mahachai Green co_,Ltd$Purch_ Rcpt_ Line" '
        'As T2 ON T1."Entry No_" = T2."Item Rcpt_ Entry No_" and T1."Document No_" = T2."Document No_" Where T1."Entry No_" > ' + str(
            erp_no) + ' AND CAST(T1."timestamp" as int) >' + str(
            timestamp) + ' Order by T1.[Entry No_]')
    total = len(cursor.fetchall())

    cursor.execute(
        'SELECT T1."timestamp",T1."Item No_",T1."Posting Date",T1."Document No_",T1."Quantity",T1."Cost Amount (Stock)",T2."Unit Cost",T1."Source No_",T1."Entry No_" '
        'FROM "Mahachai Green co_,Ltd$Item Ledger Entry" As T1 LEFT JOIN  "Mahachai Green co_,Ltd$Purch_ Rcpt_ Line" '
        'As T2 ON T1."Entry No_" = T2."Item Rcpt_ Entry No_" and T1."Document No_" = T2."Document No_" Where T1."Entry No_" > ' + str(
            erp_no) + ' AND CAST(T1."timestamp" as int) >' + str(
            timestamp) + ' Order by T1.[Entry No_]')

    row = cursor.fetchone()
    count = 1
    while row:
        print str(count) + ' / ' + str(total)
        hex2 = '0x' + str(binascii.b2a_hex(row[0]))
        time = int(hex2, 16)

        if (row[4] >= 0):
            transaction_instance = Transaction.objects.create(types=0, po=str(row[3].encode('utf-8').strip()),
                                                              erp_type=True, timestamp=time, erp_no=row[8],
                                                              date=row[2])

        else:
            transaction_instance = Transaction.objects.create(types=1, po=str(row[3].encode('utf-8').strip()),
                                                              erp_type=True, timestamp=time, erp_no=row[8],
                                                              date=row[2])

        try:
            supplier = Supplier.objects.get(ext_code=str(row[7].encode('utf-8').strip()))
        except Supplier.DoesNotExist as e:
            supplier = None

        if row[6] == None:
            cost = row[5]
        else:
            cost = row[6]

        try:
            product = Product.objects.get(ext_code=str(row[1].encode('utf-8').strip()))
            uom = product.uom
            product.valuation = decimal.Decimal(product.valuation) + row[4] * cost
            product.quantity = decimal.Decimal(product.quantity) + row[4]
            product.save()
        except Product.DoesNotExist as e:
            product = None
            uom = None

        if (row[4] >= 0):
            transaction_line_instance = InputDetail.objects.create(supplier=supplier, product=product, uom=uom,
                                                                   quantity=row[4],
                                                                   unit_price=cost,
                                                                   transaction=transaction_instance, erp_type=True,
                                                                   left_quantity=row[4],reserve_quantity=row[4], amount=row[4] * cost
                                                                   )
            transaction_line_instance.created_date = row[2]
            transaction_line_instance.save()

        else:
            transaction_line_instance = WithdrawDetail.objects.create(product=product, uom=uom,
                                                                      quantity=abs(row[4]),
                                                                      unit_price=cost,
                                                                      transaction=transaction_instance,
                                                                      amount=abs(row[4]) * cost, erp_type=True
                                                                      )
            transaction_line_instance.created_date = row[2]
            transaction_line_instance.save()

        count = count + 1
        row = cursor.fetchone()

    withdraw_stock_after_synced()


def purchase_order_rcpt_sync():
    cnxn = initconncetion()
    cursor = cnxn.cursor()

    try:
        transaction = Transaction.objects.filter(erp_type=True).order_by('-timestamp')[0]
        timestamp = str(transaction.timestamp)
    except Exception as e:
        timestamp = str(0)

    cursor.execute(
        'SELECT PO."timestamp",PO."No_",PO."Posting Date" FROM "Mahachai Green co_,Ltd$Purch_ Rcpt_ Header" '
        'As PO INNER JOIN "Mahachai Green co_,Ltd$Purch_ Rcpt_ Line" As PL ON PL."Document No_" = PO."No_" '
        'Where PL."Type" = 2 AND CAST(PO."timestamp" as int) >' + timestamp + 'GROUP By PO."No_",PO."timestamp",PO."Buy-from Vendor No_",PO."Posting Date"')
    row = cursor.fetchone()
    while row:
        try:
            transaction = Transaction.objects.get(po=str(row[1].encode('utf-8').strip()))
            hex2 = '0x' + str(binascii.b2a_hex(row[0]))
            time = int(hex2, 16)
            transaction.timestamp = time
            transaction.date = row[2]
            transaction.save()
        except Exception as e:
            hex2 = '0x' + str(binascii.b2a_hex(row[0]))
            time = int(hex2, 16)
            Transaction.objects.create(types=0, po=str(row[1].encode('utf-8').strip()), erp_type=True, timestamp=time,
                                       date=row[2]
                                       )
        row = cursor.fetchone()

# def purchase_order_rcpt_line_2sync():
#     cnxn = initconncetion()
#     cursor = cnxn.cursor()
#
#     try:
#         input_line = InputDetail.objects.filter(erp_type=True).order_by('-timestamp')[0]
#         timestamp = str(input_line.timestamp)
#     except Exception as e:
#         timestamp = str(0)
#
#     cursor.execute(
#         'SELECT "timestamp","Document No_","Line No_","Buy-from Vendor No_","No_","Quantity","Direct Unit Cost","Description","Posting Date" '
#         'FROM "Mahachai Green co_,Ltd$Purch_ Rcpt_ Line"Where  Type=2 AND CAST(timestamp as int) >' + timestamp)
#     row = cursor.fetchone()
#     while row:
#         try:
#             input_line_instance = InputDetail.objects.get(transaction__po=str(row[1].encode('utf-8').strip()),
#                                                           line_no=str(row[2].encode('utf-8').strip()))
#             try:
#                 supplier = Supplier.objects.get(ext_code=str(row[3].encode('utf-8').strip()))
#             except Supplier.DoesNotExist as e:
#                 supplier = None
#
#             try:
#                 product = Product.objects.get(ext_code=str(row[4].encode('utf-8').strip()))
#                 uom = product.uom
#                 product.quantity = decimal.Decimal(product.quantity) + row[5]
#                 product.valuation = decimal.Decimal(product.valuation) + row[5] * row[6]
#                 product.save()
#             except Product.DoesNotExist as e:
#                 product = None
#                 uom = None
#
#             hex2 = '0x' + str(binascii.b2a_hex(row[0]))
#             time = int(hex2, 16)
#             input_line_instance.timestamp = time
#             input_line_instance.supplier = supplier
#             input_line_instance.products = product
#             input_line_instance.uom = uom
#             input_line_instance.quantity = row[5]
#             input_line_instance.unit_price = row[6]
#             input_line_instance.description = str(row[7].encode('utf-8').strip())
#             input_line.created_date = row[8]
#             input_line_instance.save()
#         except Exception as e:
#             transaction_instance = Transaction.objects.get(po=str(row[1].encode('utf-8').strip()))
#
#             try:
#                 supplier = Supplier.objects.get(ext_code=str(row[3].encode('utf-8').strip()))
#             except Supplier.DoesNotExist as e:
#                 supplier = None
#
#             try:
#                 product = Product.objects.get(ext_code=str(row[4].encode('utf-8').strip()))
#                 uom = product.uom
#                 product.quantity = decimal.Decimal(product.quantity) + row[5]
#                 product.valuation = decimal.Decimal(product.valuation) + row[5] * row[6]
#                 product.save()
#             except Product.DoesNotExist as e:
#                 product = None
#                 uom = None
#
#             hex2 = '0x' + str(binascii.b2a_hex(row[0]))
#             time = int(hex2, 16)
#             input = InputDetail.objects.create(timestamp=time, supplier=supplier, product=product, uom=uom,
#                                                quantity=row[5],
#                                                unit_price=row[6],
#                                                transaction=transaction_instance, line_no=str(row[2]), erp_type=True,
#                                                left_quantity=row[5], amount=row[5] * row[6],
#                                                description=str(row[7].encode('utf-8').strip())
#                                                )
#             input.created_date = row[8]
#             input.save()
#
#         row = cursor.fetchone()
