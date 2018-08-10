from conclusion.models import PowerGeneration
from datetime import datetime, timedelta


def get_old_data(obj):
    power = PowerGeneration.objects.get(id=obj.id)
    array_date = []
    for x in str(power.created_date.date()).split('-'):
        array_date.append(x)

    date_delete_1 = datetime(year=int(array_date[0]), month=int(array_date[1]), day=int(array_date[2])) - timedelta(
        days=1)

    array_date_delete_1 = []
    for x in str(date_delete_1.date()).split('-'):
        array_date_delete_1.append(x)

    if power.hours == 1:
        try:
            old = PowerGeneration.objects.get(created_date__day=array_date_delete_1[2],
                                              created_date__month=array_date_delete_1[1],
                                              created_date__year=array_date_delete_1[0], hours=24)
        except Exception:
            old = None

    else:
        try:
            old = PowerGeneration.objects.get(created_date__day=array_date[2],
                                              created_date__month=array_date[1],
                                              created_date__year=array_date[0], hours=power.hours - 1)
        except Exception:
            old = None

    return power, old
