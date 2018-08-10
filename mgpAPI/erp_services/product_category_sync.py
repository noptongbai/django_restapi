from  mgpAPI.erp_services.conncet_database import initconncetion
from  products.models import ProductCategory
import binascii

def product_category_sync():
    cnxn = initconncetion()
    cursor = cnxn.cursor()

    try:
        product_category = ProductCategory.objects.filter(erp_type=True).order_by('-timestamp')[0]
        timestamp = str(product_category.timestamp)
    except Exception as e:
        timestamp = str(0)

    cursor.execute('SELECT * FROM "Mahachai Green co_,Ltd$Product Group" Where  CAST(timestamp as int) >'+timestamp)
    row = cursor.fetchone()
    while row:

        try:
            product_category = ProductCategory.objects.get(ext_code=str(row[2].encode('utf-8').strip()))
            hex2 = '0x' + str(binascii.b2a_hex(row[0]))
            time = int(hex2, 16)
            product_category.timestamp = time
            product_category.item_category_code = str(row[1].encode('utf-8').strip())
            product_category.description = str(row[3].encode('utf-8').strip())
            product_category.save()
        except Exception as a:
            hex2 = '0x' + str(binascii.b2a_hex(row[0]))
            time = int(hex2, 16)
            ProductCategory.objects.create(timestamp=time,title=str(row[2].encode('utf-8').strip()),
                                           ext_code=str(row[2].encode('utf-8').strip()),
                                           item_category_code=str(row[1].encode('utf-8').strip()),
                                           description=str(row[3].encode('utf-8').strip()),erp_type=True)

        row = cursor.fetchone()


