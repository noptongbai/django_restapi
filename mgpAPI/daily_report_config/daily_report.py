from conclusion.models import Outage, PowerGeneration, ManufacturingTransactionLine
from mgpAPI.serializers.daily_report import ReportDaily
from datetime import timedelta, datetime
from django.db.models import Q
from common.master_models import Preference


def add_data_daily(data):
    array_date = []
    for x in data.split('-'):
        array_date.append(x)

    date_delete_1 = datetime(year=int(array_date[0]), month=int(array_date[1]), day=int(array_date[2])) - timedelta(
        days=1)
    array_date_delete_1 = []
    for x in str(date_delete_1.date()).split('-'):
        array_date_delete_1.append(x)

    power = PowerGeneration.objects.filter(created_date__day=array_date[2], created_date__month=array_date[1],
                                           created_date__year=array_date[0])
    power_array = []
    for p in power:
        a = dict()
        a["sector"] = p.sector.title
        a["generate_meter"] = p.generate_meter
        a["export_meter"] = p.export_meter
        a["steam"] = p.steam
        a["weight_scale_meter"] = p.weight_scale_meter
        a["date"] = data
        power_array.append(a)

    manu_tran = ManufacturingTransactionLine.objects.filter(created_date__day=array_date[2],
                                                            created_date__month=array_date[1],
                                                            created_date__year=array_date[0])
    manu_tran_array = []
    for m in manu_tran:
        a = dict()
        a["product"] = m.product.title
        a["unit"] = m.product.uom.title
        a["quantity"] = m.quantity
        manu_tran_array.append(a)

    start_datetime = datetime(
        year=int(array_date[0]),
        month=int(array_date[1]),
        day=int(array_date[2])
    )

    end_datetime = datetime(
        year=int(array_date[0]),
        month=int(array_date[1]),
        day=int(array_date[2]),
        hour=23,
        minute=59,
        second=59
    )

    out = Outage.objects.filter(
        Q(through_time__range=(start_datetime, end_datetime)) | Q(from_time__range=(start_datetime, end_datetime)))
    out_array = []
    for o in out:
        a = dict()
        if o.planned_outage == 0:
            plan = "plan"
        elif o.planned_outage == 1:
            plan = "unplan"
        else:
            plan = "variability"
        a["planned_outage"] = plan
        a["note"] = o.note
        a["from_time"] = o.from_time
        a["through_time"] = o.through_time
        out_array.append(a)

    generation_date_array = []
    generation_hour_array = []
    generation_date = dict()
    sum_all = 0
    sum_all2 = 0
    sum_all3 = 0
    try:
        pref = Preference.objects.get(key="steam_factor")
        value = float(pref.value)
    except Exception:
        value = 3.6

    for i in range(24):
        generation_hour = dict()
        if i == 0:
            before = PowerGeneration.objects.filter(created_date__day=array_date_delete_1[2],
                                                    created_date__month=array_date_delete_1[1],
                                                    created_date__year=array_date_delete_1[0], hours=24)

            after = PowerGeneration.objects.filter(created_date__day=array_date[2], created_date__month=array_date[1],
                                                   created_date__year=array_date[0], hours=i + 1)

            if len(before) > 0 and len(after) > 0:
                before = before[0]
                after = after[0]
                generation_hour["hour"] = i + 1
                check = after.export_meter - before.export_meter
                check2 = after.generate_meter - before.generate_meter
                check3 = after.steam * value
                generation_hour["accumulate_net"] = check
                generation_hour["accumulate_gross"] = check2
                generation_hour["main_steam_consumption"] = check3
                generation_hour_array.append(generation_hour)
                sum_all = sum_all + check
                sum_all2 = sum_all2 + check2
                sum_all3 = sum_all3 + check3
            elif len(after) > 0:
                after = after[0]
                generation_hour["hour"] = i + 1
                check = after.export_meter
                check2 = after.generate_meter
                check3 = after.steam * value
                generation_hour["accumulate_net"] = check
                generation_hour["accumulate_gross"] = check2
                generation_hour["main_steam_consumption"] = check3
                generation_hour_array.append(generation_hour)
                sum_all = sum_all + check
                sum_all2 = sum_all2 + check2
                sum_all3 = sum_all3 + check3
            elif len(before) > 0:
                before = before[0]
                check = - before.export_meter
                check2 = - before.generate_meter
                generation_hour["hour"] = i + 1
                generation_hour["accumulate_net"] = check
                generation_hour["accumulate_gross"] = check2
                generation_hour["main_steam_consumption"] = 0
                generation_hour_array.append(generation_hour)
            else:
                generation_hour["hour"] = i + 1
                generation_hour["accumulate_net"] = 0
                generation_hour["accumulate_gross"] = 0
                generation_hour["main_steam_consumption"] = 0
                generation_hour_array.append(generation_hour)

        else:
            before = PowerGeneration.objects.filter(created_date__day=array_date[2],
                                                    created_date__month=array_date[1],
                                                    created_date__year=array_date[0], hours=i)

            after = PowerGeneration.objects.filter(created_date__day=array_date[2], created_date__month=array_date[1],
                                                   created_date__year=array_date[0], hours=i + 1)

            if len(before) > 0 and len(after) > 0:

                before = before[0]

                after = after[0]

                generation_hour["hour"] = i + 1
                check = after.export_meter - before.export_meter
                check2 = after.generate_meter - before.generate_meter
                check3 = after.steam * value
                generation_hour["accumulate_net"] = check
                generation_hour["accumulate_gross"] = check2
                generation_hour["main_steam_consumption"] = check3
                generation_hour_array.append(generation_hour)
                sum_all = sum_all + check
                sum_all2 = sum_all2 + check2
                sum_all3 = sum_all3 + check3
            elif len(after) > 0:
                after = after[0]
                generation_hour["hour"] = i + 1
                check = after.export_meter
                check2 = after.generate_meter
                check3 = after.steam * value
                generation_hour["accumulate_net"] = check
                generation_hour["accumulate_gross"] = check2
                generation_hour["main_steam_consumption"] = check3
                generation_hour_array.append(generation_hour)
                sum_all = sum_all + check
                sum_all2 = sum_all2 + check2
                sum_all3 = sum_all3 + check3
            elif len(before) > 0:
                before = before[0]
                check = - before.export_meter
                check2 = - before.generate_meter
                generation_hour["hour"] = i + 1
                generation_hour["accumulate_net"] = check
                generation_hour["accumulate_gross"] = check2
                generation_hour["main_steam_consumption"] = 0
                generation_hour_array.append(generation_hour)
            else:
                generation_hour["hour"] = i + 1
                generation_hour["accumulate_net"] = 0
                generation_hour["accumulate_gross"] = 0
                generation_hour["main_steam_consumption"] = 0
                generation_hour_array.append(generation_hour)

    generation_date["date"] = data
    generation_date["accumulate_net"] = sum_all
    generation_date["accumulate_gross"] = sum_all2
    generation_date["main_steam_consumption"] = sum_all3
    generation_date_array.append(generation_date)

    report_all = {
        1: ReportDaily(
            date=data,
            products_consumption=manu_tran_array,
            outages=out_array,
            generation=power_array,
            energy_hours=generation_hour_array,
            energy_dates=generation_date_array
        ),

    }

    return report_all
