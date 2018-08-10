from  mgpAPI.erp_services.conncet_database import initconncetion
from  common.master_models import Supplier
import binascii

def vendor_sync():
    cnxn = initconncetion()
    cursor = cnxn.cursor()
    try:
        supplier = Supplier.objects.all().order_by('-timestamp')[0]
        timestamp = str(supplier.timestamp)
    except Exception as e:
        timestamp = str(0)

    cursor.execute('SELECT * FROM "Mahachai Green co_,Ltd$Vendor"Where  CAST(timestamp as int) >'+timestamp)
    row = cursor.fetchone()
    while row:
        try:
            supplier = Supplier.objects.get(ext_code=str(row[1].encode('utf-8').strip()))
            hex2 = '0x' + str(binascii.b2a_hex(row[0]))
            time = int(hex2, 16)
            supplier.timestamp = time
            supplier.description = str(row[2].encode('utf-8').strip())
            supplier.save()
        except Exception as a:
            hex2 = '0x' + str(binascii.b2a_hex(row[0]))
            time = int(hex2, 16)
            Supplier.objects.create(timestamp=time,title=str(row[2].encode('utf-8').strip()),
                                       ext_code=str(row[1].encode('utf-8').strip()),
                                       description=str(row[2].encode('utf-8').strip()))

        row = cursor.fetchone()

