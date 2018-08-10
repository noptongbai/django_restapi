from  mgpAPI.erp_services.conncet_database import initconncetion
from  transactions.models import TransactionLog
from datetime import datetime, timedelta


def transaction_log_sync():
    """ insert Jounal template,Jounal Batch Name,Line No_,Item No_,Posting Date,Description,Location Code,Invenroy PostingGroup,Quantity"""

    cnxn = initconncetion()
    cursor = cnxn.cursor()
    rows = []
    transactionlogs = TransactionLog.objects.filter(synced=False)

    for transactionlog in transactionlogs:
        if transactionlog.quantity >= 0:
            message = 'POSITIVE'
            entry = 2
        else:
            message = 'NEGATIVE'
            entry = 3

        row = ['ITEM', message, transactionlog.lines, transactionlog.product.ext_code,
               transactionlog.last_modified_date.date(),
               # 1
               abs(transactionlog.quantity), transactionlog.unit_price, entry, "ITEMJNL", "",  # 2
               transactionlog.product.title, "MGP", transactionlog.product.product_category.ext_code,
               transactionlog.last_modified_date.date(), 0.0,
               # 3
               transactionlog.unit_price, transactionlog.unit_price * abs(transactionlog.quantity), 0.0,
               "1753-01-01 00:00:00", "1753-01-01 00:00:00",
               # 4
               0, 0, "1753-01-01 00:00:00", "1753-01-01 00:00:00", 0.0,  # 5
               0, "1753-01-01 00:00:00", 0, "1753-01-01 00:00:00", "1753-01-01 00:00:00",  # 6
               0, "1753-01-01 00:00:00", "", "", "",  # 7
               "", "", 0.0, 0.0, 0,  # 8
               0, "", "", "", "",  # 9
               "", "", "", "", 0.0,  # 10
               "", 0, 0, 0, "",  # 11
               0, 0, 0, 0, "",  # 12
               "", 0, 0, "", "",  # 13
               0.0, "", transactionlog.product.uom.title, 0, 0.0,  # 14
               0.0, 0, 0, 0, "",  # 15
               "", "", 0, "", 0,  # 16
               "", "", "", "", 0,  # 17
               "", 0.0, 0.0, 0, 0,  # 18
               0, 0, "", 0.0, 0.0,  # 19
               0.0, 0, 0.0, 0, 0,  # 20
               0, "", 0, "", "",  # 21
               "", 0.0, 0.0, 0.0, 0.0,  # 22
               0.0, 0.0, 0.0, 0.0, 0.0,  # 23
               0.0, 0.0, "", 0.0, "",  # 24
               "", "", 0, 0, 0,  # 25
               0, 0, "", "", "",  # 26
               "", "", "", "", "",  # 27
               "", "", "", "", 0,  # 28
               "", 0, "", "", "",  # 29
               0.0, 0.0, 0.0, 0.0, 0.0,  # 30
               0.0, 0.0, 0.0, 0.0, 0.0,  # 31
               0.0]  # 32

        rows.append(row)
        transactionlog.synced = True
        transactionlog.save()

    if (len(rows) > 0):
        cursor.executemany(
            'INSERT INTO "Mahachai Green co_,Ltd$Item Journal Line" '
            '("Journal Template Name","Journal Batch Name","Line No_","Item No_","Posting Date",'  # 1

            '"Quantity","Unit Cost","Entry Type","Source Code","Document No_",'  # 2

            '"Description","Location Code","Inventory Posting Group","Document Date","Invoiced Quantity",'  # 3

            '"Unit Amount","Amount","Discount Amount","Expiration Date" ,"Planned Delivery Date",'  # 4

            '"Applies-to Entry","Item Shpt_ Entry No_","Order Date","Warranty Date","Indirect Cost _",'  # 5

            '"Source Type","New Item Expiration Date","Recurring Method","Item Expiration Date","Starting Time",'  # 6

            '"Drop Shipment","Ending Time","Transport Method","Country_Region Code","New Location Code",'  # 7

            '"New Shortcut Dimension 1 Code","New Shortcut Dimension 2 Code","Qty_ (Calculated)","Qty_ (Phys_ Inventory)","Last Item Ledger Entry No_",'  # 8

            '"Phys_ Inventory","Gen_ Bus_ Posting Group","Gen_ Prod_ Posting Group","Entry_Exit Point","Source Posting Group",'  # 9

            '"External Document No_","Area","Transaction Specification","Posting No_ Series","Unit Cost (ACY)",'  # 10

            '"Source Currency Code","Document Type","Document Line No_","Order Type","Order No_",'  # 11

            '"Order Line No_","Dimension Set ID","New Dimension Set ID","Assemble to Order","Job No_",'  # 12

            '"Job Task No_","Job Purchase","Job Contract Entry No_","Variant Code","Bin Code",'  # 13

            '"Qty_ per Unit of Measure","New Bin Code","Unit of Measure Code","Derived from Blanket Order","Quantity (Base)",'  # 14

            '"Invoiced Qty_ (Base)","Level","Flushing Method","Changed by User","Cross-Reference No_",'  # 15

            '"Originally Ordered No_","Originally Ordered Var_ Code","Out-of-Stock Substitution","Item Category Code","Nonstock",'  # 16

            '"Purchasing Code","Product Group Code","Source No_","Shortcut Dimension 1 Code","Value Entry Type",'  # 17

            '"Item Charge No_","Inventory Value (Calculated)","Inventory Value (Revalued)","Variance Type","Inventory Value Per",'  # 18

            '"Partial Revaluation","Applies-from Entry","Invoice No_","Unit Cost (Calculated)","Unit Cost (Revalued)",'  # 19

            '"Applied Amount","Update Standard Cost","Amount (ACY)","Correction","Adjustment",'  # 20

            '"Applies-to Value Entry","Invoice-to Source No_","Type","No_","Operation No_",'  # 21

            '"Work Center No_","Setup Time","Run Time","Stop Time","Output Quantity",'  # 22

            '"Scrap Quantity","Concurrent Capacity","Setup Time (Base)","Run Time (Base)","Stop Time (Base)",'  # 23

            '"Output Quantity (Base)","Scrap Quantity (Base)","Cap_ Unit of Measure Code","Qty_ per Cap_ Unit of Measure","Recurring Frequency",'  # 24

            '"Transaction Type","Routing No_","Routing Reference No_","Prod_ Order Comp_ Line No_","Finished",'  # 25 

            '"Unit Cost Calculation","Subcontracting","Stop Code","Scrap Code","Work Center Group Code",'  # 26

            '"Work Shift Code","Serial No_","Lot No_","Shortcut Dimension 2 Code","New Serial No_",'  # 27

            '"New Lot No_","Reason Code","Salespers__Purch_ Code","Return Reason Code","Warehouse Adjustment",'  # 28

            '"Phys Invt Counting Period Code","Phys Invt Counting Period Type","Customer No_","Document No_ Series","Remark",'  # 29

            '"Overhead Rate","Single-Level Material Cost","Single-Level Capacity Cost","Single-Level Subcontrd_ Cost","Single-Level Cap_ Ovhd Cost",'  # 30

            '"Single-Level Mfg_ Ovhd Cost","Rolled-up Material Cost","Rolled-up Capacity Cost","Rolled-up Subcontracted Cost","Rolled-up Mfg_ Ovhd Cost",'  # 31

            '"Rolled-up Cap_ Overhead Cost")VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'  # 32
            '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s'
            ',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',

            rows)
        # cursor.commit()
        # cnxn.commit()
