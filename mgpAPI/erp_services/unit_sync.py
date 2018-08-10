from  mgpAPI.erp_services.conncet_database import initconncetion
from  units.models import Unit
import binascii


def unit_sync():
    cnxn = initconncetion()
    cursor = cnxn.cursor()

    try:
        unit = Unit.objects.all().order_by('-timestamp')[0]
        timestamp = str(unit.timestamp)
    except Exception as e:
        timestamp = str(0)

    cursor.execute('SELECT * FROM "Mahachai Green co_,Ltd$Unit of Measure"Where  CAST(timestamp as int) >'+timestamp)
    row = cursor.fetchone()
    while row:

        try:
            unit = Unit.objects.get(ext_code=str(row[1].encode('utf-8').strip()))
            hex2 = '0x' + str(binascii.b2a_hex(row[0]))
            time = int(hex2, 16)
            unit.timestamp = time
            unit.description = str(row[2].encode('utf-8').strip())
            unit.save()
        except Exception as a:
            hex2 = '0x' + str(binascii.b2a_hex(row[0]))
            time = int(hex2, 16)
            Unit.objects.create(timestamp= time, unit_category_id=1, title=str(row[1].encode('utf-8').strip()),
                                ext_code=str(row[1].encode('utf-8').strip()),
                                description=str(row[2].encode('utf-8').strip()))

        row = cursor.fetchone()
