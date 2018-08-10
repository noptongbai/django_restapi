from conclusion.models import Outage, PowerGeneration, ManufacturingTransactionLine
from mgpAPI.serializers.daily_report import ReportDaily
from date_to_month import date_to_month
from datetime import timedelta, datetime
import calendar


def add_data_month(data):
    array_date = []
    for x in data.split('-'):
        array_date.append(x)

    end = calendar.monthrange(int(array_date[0]), int(array_date[1]))[1]
    print end

    array_data = dict()
    for x in range(1, end + 1):
        a = array_date[0] + '-' + array_date[1] + '-' + str(x)
        data_convert = date_to_month(a)
        array_data.update({x:data_convert})



    report_all = {
        1: ReportDaily(
            month=data,
            each_date=[ReportDaily(
                date=data)]
        ),
        2: ReportDaily(
            month=data,
            each_date=[ReportDaily(
                date=data)]
        )
    }

    return array_data
