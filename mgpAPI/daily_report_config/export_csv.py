import csv, os
from django.conf import settings
from django.http import HttpResponse
from datetime import datetime
from mgpAPI.serializers.daily_report import ReportDailyDateSerializer


def create_file_date(file):
    serializer = ReportDailyDateSerializer(instance=file.values(), many=True)
    for a in serializer.data:
        print a["date"]
        # print a["products_consumption"]
        # print a["outages"]
        # print a["generation"]
        # print a["energy_hours"]
        # print a["energy_dates"]
    file_name = str((datetime.now() - datetime(1970, 1, 1)).total_seconds()) + "_export_date.csv"
    with open(os.path.join(settings.MEDIA_ROOT + 'static', file_name), 'w') as f:
        wr = csv.writer(f, lineterminator='\n')
        wr.writerow([a["date"]])
        wr.writerow(["Time","Accumulate Net","Main Steam Consumption","Accumulate Gross"])
        for b in a["energy_hours"]:
            con = str(b['hour']) + '.00'
            con = "%.2f" % float(con)
            print con
            wr.writerow([con,str(b['accumulate_net']),str(b['main_steam_consumption']),str(b['accumulate_gross'])])
        for c in a["energy_dates"]:
            wr.writerow(['Sum Accumulate Net', str(c['accumulate_net']),'Main Steam Consumption',str(c['main_steam_consumption']),'Accumulate Gross',str(c['accumulate_gross'])])
    return file_name


def create_file_month(file):
    serializer = ReportDailyDateSerializer(instance=file.values(), many=True)

    file_name = str((datetime.now() - datetime(1970, 1, 1)).total_seconds()) + "_export_date.csv"
    with open(os.path.join(settings.MEDIA_ROOT + 'static', file_name), 'w') as f:
        wr = csv.writer(f, lineterminator='\n')
        for a in serializer.data:
            wr.writerow([a["date"]])
            wr.writerow(["Time", "Accumulate Net"])
            for b in a["energy_hours"]:
                con = str(b['hour']) + '.00'
                con = "%.2f" % float(con)
                print con
                wr.writerow([con, str(b['accumulate_net']),str(b['main_steam_consumption']),str(b['accumulate_gross'])])
            for c in a["energy_dates"]:
                wr.writerow(['Sum Accumulate Net', str(c['accumulate_net']),'Main Steam Consumption',str(c['main_steam_consumption']),'Accumulate Gross',str(c['accumulate_gross'])])
    return file_name
