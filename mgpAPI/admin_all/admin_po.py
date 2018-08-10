from django.contrib import admin
from purchase_orders.models import PurchaseOrder,PurchaseOrderLine

class PurchaseOrderInLineAdmin(admin.TabularInline):
    model = PurchaseOrderLine
    extra = 0
    raw_id_fields = ("product","supplier","uom")

@admin.register(PurchaseOrder)
class PurchaseAdmin(admin.ModelAdmin):
    inlines = [
        PurchaseOrderInLineAdmin,
    ]