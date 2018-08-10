from rest_framework import serializers
from conclusion.models import PowerGeneration, Outage
from transactions.models import InputDetail, WithdrawDetail
from datetime import datetime
from django.db.models import Q
from django.db.models import Sum


def me(data, range_date, start, end):
    array_single = []

    while start != end:
        if range_date == 12:
            all = PowerGeneration.objects.filter(created_date__year=start)

            sum_data = all.aggregate(Sum('export_meter'))['export_meter__sum']

            if sum_data == None:
                sum_data = 0

            array_single.append(sum_data)
            start = start + 1

        elif range_date == 3:

            all = PowerGeneration.objects.filter(Q(created_date__month=1) | Q(created_date__month=2) |
                                                 Q(created_date__month=3),
                                                 created_date__year=start)
            sum_data = all.aggregate(Sum('export_meter'))['export_meter__sum']
            if sum_data == None:
                sum_data = 0
            array_single.append(sum_data)

            all = PowerGeneration.objects.filter(Q(created_date__month=4) | Q(created_date__month=5) |
                                                 Q(created_date__month=6),
                                                 created_date__year=start)
            sum_data = all.aggregate(Sum('export_meter'))['export_meter__sum']
            if sum_data == None:
                sum_data = 0
            array_single.append(sum_data)

            all = PowerGeneration.objects.filter(Q(created_date__month=7) | Q(created_date__month=8) |
                                                 Q(created_date__month=9),
                                                 created_date__year=start)
            sum_data = all.aggregate(Sum('export_meter'))['export_meter__sum']
            if sum_data == None:
                sum_data = 0
            array_single.append(sum_data)

            all = PowerGeneration.objects.filter(Q(created_date__month=10) | Q(created_date__month=11) |
                                                 Q(created_date__month=12),
                                                 created_date__year=start)
            sum_data = all.aggregate(Sum('export_meter'))['export_meter__sum']
            if sum_data == None:
                sum_data = 0
            array_single.append(sum_data)

            start = start + 1
        else:
            for i in range(12):
                all = PowerGeneration.objects.filter(created_date__month=i + 1,
                                                     created_date__year=start)
                sum_data = all.aggregate(Sum('export_meter'))['export_meter__sum']

                if sum_data == None:
                    sum_data = 0
                array_single.append(sum_data)

            start = start + 1

    return array_single
