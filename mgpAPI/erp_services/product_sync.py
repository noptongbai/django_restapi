from  mgpAPI.erp_services.conncet_database import initconncetion
from  products.models import Product, ProductCategory
from  units.models import Unit
import binascii


def product_sync():
    cnxn = initconncetion()
    cursor = cnxn.cursor()

    try:
        product = Product.objects.filter(erp_type=True).order_by('-timestamp')[0]
        timestamp = str(product.timestamp)
    except Exception as e:
        timestamp = str(0)

    cursor.execute(
        'SELECT "timestamp","No_","Description","Base Unit of Measure","Inventory Posting Group","Description 2" FROM "Mahachai Green co_,Ltd$Item"Where  CAST(timestamp as int) >' + timestamp)
    row = cursor.fetchone()
    while row:
        try:
            product = Product.objects.get(ext_code=str(row[1].encode('utf-8').strip()))
            hex2 = '0x' + str(binascii.b2a_hex(row[0]))
            time = int(hex2, 16)
            try:
                product_category = ProductCategory.objects.get(ext_code=str(row[4].encode('utf-8').strip()))
            except Exception as E:
                product_category = None

            try:
                unit = Unit.objects.get(ext_code=str(row[3].encode('utf-8').strip()))
            except Exception as E:
                unit = None

            product.timestamp = time
            product.product_category = product_category
            product.unit = unit
            product.title = str(row[2].encode('utf-8').strip())
            product.title2 = str(row[5].encode('utf-8').strip())
            product.description = str(row[2].encode('utf-8').strip())
            product.save()

        except Exception as a:
            hex2 = '0x' + str(binascii.b2a_hex(row[0]))
            time = int(hex2, 16)

            if len(ProductCategory.objects.filter(ext_code=str(row[4].encode('utf-8').strip()))) == 1:
                product_category = ProductCategory.objects.get(ext_code=str(row[4].encode('utf-8').strip()))
            else:
                product_category = None

            unit = Unit.objects.get(ext_code=str(row[3].encode('utf-8').strip()))
            Product.objects.create(timestamp=time, ext_code=str(row[1].encode('utf-8').strip()),
                                   title=str(row[2].encode('utf-8').strip()),
                                   description=str(row[2].encode('utf-8').strip()), uom=unit,
                                   product_category=product_category, erp_type=True,
                                   title2=str(row[5].encode('utf-8').strip()))

        row = cursor.fetchone()
