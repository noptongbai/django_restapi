from threading import Lock

from mgpAPI.erp_services.product_sync import product_sync
from mgpAPI.erp_services.vendor_sync import vendor_sync
from mgpAPI.erp_services.product_category_sync import product_category_sync
from mgpAPI.erp_services.unit_sync import unit_sync
from mgpAPI.erp_services.po_sync import purchase_order_line_sync, purchase_order_sync
from mgpAPI.erp_services.po_rcpt_sync import purchase_order_rcpt_line_sync, purchase_order_rcpt_sync


lock = Lock()


def syncall():
    lock.acquire()  # will block if another thread has lock
    try:
        product_category_sync()
        unit_sync()
        vendor_sync()
        product_sync()
        purchase_order_sync()
        purchase_order_line_sync()
        purchase_order_rcpt_line_sync()

    finally:
        lock.release()
