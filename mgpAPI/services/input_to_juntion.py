from  transactions.models import InputJuntionWithdraw, InputJuntionScrap, InputJuntionReturn, InputJuntionAdjust


def input_juntion(input_instance, withdraw_instance, type, quantity, date, note, supplier):
    if type == 1:
        InputJuntionWithdraw.objects.create(input_transaction=input_instance, withdraw_transaction=withdraw_instance,
                                            quantity=quantity, date=date, note=note, supplier=supplier)
    elif type == 2:
        InputJuntionScrap.objects.create(input_transaction=input_instance, scrap_transaction=withdraw_instance,
                                         quantity=quantity, date=date, note=note, supplier=supplier)
    elif type == 3:
        InputJuntionReturn.objects.create(input_transaction=input_instance, return_transaction=withdraw_instance,
                                          quantity=quantity, date=date, note=note, supplier=supplier)
    elif type == 4:
        InputJuntionAdjust.objects.create(input_transaction=input_instance, adjust_transaction=withdraw_instance,
                                          quantity=quantity, date=date, note=note, supplier=supplier)
