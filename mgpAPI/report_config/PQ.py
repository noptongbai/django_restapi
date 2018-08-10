from rest_framework import serializers
from conclusion.models import PowerGeneration, Outage
from transactions.models import InputDetail, WithdrawDetail
from datetime import datetime
from transactions.models import InputDetail
from django.db.models import Q
from django.db.models import Sum


def pq(data, range_date, start, end):
    id = int(data.split("PQ")[1])

    array_single = []
    while start != end:
        if range_date == 12:
            all_t = InputDetail.objects.filter(created_date__year=start, product__id=id, erp_type=True)
            all_w = WithdrawDetail.objects.filter(created_date__year=start, product__id=id, erp_type=True)

            sum_t = all_t.aggregate(Sum('quantity'))['quantity__sum']
            sum_w = all_w.aggregate(Sum('quantity'))['quantity__sum']
            if sum_t == None:
                sum_t = 0
            if sum_w == None:
                sum_w = 0

            sum_data = sum_t - sum_w
            array_single.append(sum_data)
            start = start + 1
        elif range_date == 3:

            all_t = InputDetail.objects.filter(Q(created_date__month=1) | Q(created_date__month=2) |
                                               Q(created_date__month=3),
                                               product__id=id, created_date__year=start, erp_type=True)

            all_w = WithdrawDetail.objects.filter(Q(created_date__month=1) | Q(created_date__month=2) |
                                                  Q(created_date__month=3),
                                                  product__id=id, created_date__year=start, erp_type=True)
            sum_t = all_t.aggregate(Sum('quantity'))['quantity__sum']
            sum_w = all_w.aggregate(Sum('quantity'))['quantity__sum']
            if sum_t == None:
                sum_t = 0
            if sum_w == None:
                sum_w = 0

            sum_data = sum_t - sum_w
            array_single.append(sum_data)

            all_t = InputDetail.objects.filter(Q(created_date__month=4) | Q(created_date__month=5) |
                                               Q(created_date__month=6),
                                               product__id=id, created_date__year=start, erp_type=True)

            all_w = WithdrawDetail.objects.filter(Q(created_date__month=4) | Q(created_date__month=5) |
                                                  Q(created_date__month=6),
                                                  product__id=id, created_date__year=start, erp_type=True)
            sum_t = all_t.aggregate(Sum('quantity'))['quantity__sum']
            sum_w = all_w.aggregate(Sum('quantity'))['quantity__sum']
            if sum_t == None:
                sum_t = 0
            if sum_w == None:
                sum_w = 0

            sum_data = sum_t - sum_w
            array_single.append(sum_data)

            all_t = InputDetail.objects.filter(Q(created_date__month=7) | Q(created_date__month=8) |
                                               Q(created_date__month=9),
                                               product__id=id, created_date__year=start, erp_type=True)

            all_w = WithdrawDetail.objects.filter(Q(created_date__month=7) | Q(created_date__month=8) |
                                                  Q(created_date__month=9),
                                                  product__id=id, created_date__year=start, erp_type=True)
            sum_t = all_t.aggregate(Sum('quantity'))['quantity__sum']
            sum_w = all_w.aggregate(Sum('quantity'))['quantity__sum']
            if sum_t == None:
                sum_t = 0
            if sum_w == None:
                sum_w = 0

            sum_data = sum_t - sum_w
            array_single.append(sum_data)

            all_t = InputDetail.objects.filter(Q(created_date__month=10) | Q(created_date__month=11) |
                                               Q(created_date__month=12),
                                               product__id=id, created_date__year=start, erp_type=True)

            all_w = WithdrawDetail.objects.filter(Q(created_date__month=10) | Q(created_date__month=11) |
                                                  Q(created_date__month=12),
                                                  product__id=id, created_date__year=start, erp_type=True)
            sum_t = all_t.aggregate(Sum('quantity'))['quantity__sum']
            sum_w = all_w.aggregate(Sum('quantity'))['quantity__sum']
            if sum_t == None:
                sum_t = 0
            if sum_w == None:
                sum_w = 0

            sum_data = sum_t - sum_w
            array_single.append(sum_data)

            start = start + 1

        else:
            for i in range(12):
                all_t = InputDetail.objects.filter(created_date__month=i + 1,
                                                   product__id=id, created_date__year=start, erp_type=True)
                all_w = WithdrawDetail.objects.filter(created_date__month=i + 1,
                                                      product__id=id, created_date__year=start, erp_type=True)

                sum_t = all_t.aggregate(Sum('quantity'))['quantity__sum']
                sum_w = all_w.aggregate(Sum('quantity'))['quantity__sum']
                if sum_t == None:
                    sum_t = 0
                if sum_w == None:
                    sum_w = 0

                sum_data = sum_t - sum_w
                array_single.append(sum_data)

            start = start + 1

    return array_single
