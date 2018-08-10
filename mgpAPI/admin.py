from django.contrib import admin

from django.contrib.sessions.models import Session
from  common.master_models import Preference, Sector, Supplier
from  products.models import ProductCategory, Product
from  units.models import UnitCategory, Unit
from  transactions.models import InputDetail, Transaction, WithdrawDetail, ReturnDetail, ScrapDetail, AdjustDetail, \
    UnitCostHistory, InputJuntionReturn, InputJuntionScrap, InputJuntionWithdraw, TransactionLog
from  conclusion.models import ManufacturingTransaction, ManufacturingTransactionLine, Outage, PowerGeneration
from  purchase_orders.models import PurchaseOrderLine, PurchaseOrder
from mgpAPI.admin_all.admin_po import PurchaseAdmin
from mgpAPI.admin_all.admin_rcpt import TransactionInputAdmin, TransactionInputLineAdmin
from mgpAPI.admin_all.admin_product import ProductAdmin

admin.site.register(Session)
admin.site.register(Preference)
admin.site.register(Sector)
admin.site.register(Supplier)

admin.site.register(ProductCategory)

admin.site.register(UnitCategory)
admin.site.register(Unit)

# admin.site.register(Transaction)
# admin.site.register(InputDetail)
# admin.site.register(WithdrawDetail)
admin.site.register(ScrapDetail)
admin.site.register(ReturnDetail)
admin.site.register(AdjustDetail)
admin.site.register(InputJuntionReturn)
admin.site.register(InputJuntionScrap)
admin.site.register(InputJuntionWithdraw)
admin.site.register(UnitCostHistory)
admin.site.register(TransactionLog)

admin.site.register(ManufacturingTransaction)
admin.site.register(ManufacturingTransactionLine)
admin.site.register(Outage)
admin.site.register(PowerGeneration)

# admin.site.register(PurchaseOrder)
admin.site.register(PurchaseOrderLine)
