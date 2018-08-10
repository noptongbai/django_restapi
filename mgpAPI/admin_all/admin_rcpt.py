from django.contrib import admin
from transactions.models import Transaction, InputDetail,WithdrawDetail


class TransactionnInLineAdmin(admin.TabularInline):
    model = InputDetail
    extra = 0
    raw_id_fields = ("product", "supplier", "uom")

class TransactionnInLineWithdrawAdmin(admin.TabularInline):
    model = WithdrawDetail
    extra = 0
    raw_id_fields = ("product", "supplier", "uom")

@admin.register(Transaction)
class TransactionInputAdmin(admin.ModelAdmin):
    inlines = [
        TransactionnInLineAdmin,
    ]
    list_display = ('id','po')
    search_fields = ('po',)


@admin.register(InputDetail)
class TransactionInputLineAdmin(admin.ModelAdmin):
    list_filter = ("product",)
    list_display = ('id','product','uom','quantity','unit_price','amount','left_quantity','reserve_quantity','created_date')

@admin.register(WithdrawDetail)
class TransactionnInLineWithdrawAdmin(admin.ModelAdmin):
    list_filter = ("product",)
    list_display = ('id','product','uom','quantity','unit_price','used','erp_type','created_date')