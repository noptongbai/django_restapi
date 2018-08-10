from rest_framework import serializers
from conclusion.models import PowerGeneration, Outage
from transactions.models import InputDetail, WithdrawDetail
from datetime import datetime, date
from django.db.models import Q
from time import mktime
from django.db.models import Sum


def o(data, range_date, start, end):
    # a = InputDetail.objects.filter(Q(created_date__month=1) | Q(created_date__month=2),
    #                                Q(created_date__month=3) | Q(created_date__month=4),
    #                                Q(created_date__month=5) | Q(created_date__month=6),
    #                                product__id=id, created_date__year=start)
    # for c in a:
    #     print c.created_date
    array_single = []

    while start != end:
        if range_date == 12:
            start_datetime = datetime(
                year=start,
                month=1,
                day=1
            )

            end_datetime = datetime(
                year=start,
                month=12,
                day=31,
                hour=23,
                minute=59,
                second=59
            )

            all = Outage.objects.filter(from_time__range=(start_datetime, end_datetime),
                                        through_time__range=(start_datetime, end_datetime))
            all2 = Outage.objects.filter(from_time__lt=start_datetime,
                                         through_time__range=(start_datetime, end_datetime))
            all3 = Outage.objects.filter(from_time__range=(start_datetime, end_datetime),
                                         through_time__gt=end_datetime)

            sum_data = 0
            for a in all:
                diff = abs(mktime(a.from_time.timetuple()) - mktime(a.through_time.timetuple()))
                convert_to_hour = diff / 3600
                sum_data = sum_data + convert_to_hour

            for a in all2:
                diff = abs(mktime(start_datetime.timetuple()) - mktime(a.through_time.timetuple()))
                convert_to_hour = diff / 3600
                sum_data = sum_data + convert_to_hour

            for a in all3:
                diff = abs(mktime(a.from_time.timetuple()) - mktime(end_datetime.timetuple()))
                convert_to_hour = diff / 3600
                sum_data = sum_data + convert_to_hour

            array_single.append(sum_data)
            start = start + 1
        elif range_date == 3:

            start_datetime = datetime(
                year=start,
                month=1,
                day=1
            )

            end_datetime = datetime(
                year=start,
                month=3,
                day=31,
                hour=23,
                minute=59,
                second=59
            )
            all = Outage.objects.filter(from_time__range=(start_datetime, end_datetime),
                                        through_time__range=(start_datetime, end_datetime))
            all2 = Outage.objects.filter(from_time__lt=start_datetime,
                                         through_time__range=(start_datetime, end_datetime))
            all3 = Outage.objects.filter(from_time__range=(start_datetime, end_datetime),
                                         through_time__gt=end_datetime)

            sum_data = 0
            for a in all:
                diff = abs(mktime(a.from_time.timetuple()) - mktime(a.through_time.timetuple()))
                convert_to_hour = diff / 3600
                sum_data = sum_data + convert_to_hour

            for a in all2:
                diff = abs(mktime(start_datetime.timetuple()) - mktime(a.through_time.timetuple()))
                convert_to_hour = diff / 3600
                sum_data = sum_data + convert_to_hour

            for a in all3:
                diff = abs(mktime(a.from_time.timetuple()) - mktime(end_datetime.timetuple()))
                convert_to_hour = diff / 3600
                sum_data = sum_data + convert_to_hour

            array_single.append(sum_data)

            start_datetime = datetime(
                year=start,
                month=4,
                day=1
            )

            end_datetime = datetime(
                year=start,
                month=6,
                day=30,
                hour=23,
                minute=59,
                second=59
            )
            all = Outage.objects.filter(from_time__range=(start_datetime, end_datetime),
                                        through_time__range=(start_datetime, end_datetime))
            all2 = Outage.objects.filter(from_time__lt=start_datetime,
                                         through_time__range=(start_datetime, end_datetime))
            all3 = Outage.objects.filter(from_time__range=(start_datetime, end_datetime),
                                         through_time__gt=end_datetime)

            sum_data = 0

            for a in all:
                diff = abs(mktime(a.from_time.timetuple()) - mktime(a.through_time.timetuple()))
                convert_to_hour = diff / 3600
                sum_data = sum_data + convert_to_hour

            for a in all2:
                diff = abs(mktime(start_datetime.timetuple()) - mktime(a.through_time.timetuple()))
                convert_to_hour = diff / 3600
                sum_data = sum_data + convert_to_hour

            for a in all3:
                diff = abs(mktime(a.from_time.timetuple()) - mktime(end_datetime.timetuple()))
                convert_to_hour = diff / 3600
                sum_data = sum_data + convert_to_hour

            array_single.append(sum_data)
            start_datetime = datetime(
                year=start,
                month=7,
                day=1
            )

            end_datetime = datetime(
                year=start,
                month=9,
                day=30,
                hour=23,
                minute=59,
                second=59
            )
            all = Outage.objects.filter(from_time__range=(start_datetime, end_datetime),
                                        through_time__range=(start_datetime, end_datetime))
            all2 = Outage.objects.filter(from_time__lt=start_datetime,
                                         through_time__range=(start_datetime, end_datetime))
            all3 = Outage.objects.filter(from_time__range=(start_datetime, end_datetime),
                                         through_time__gt=end_datetime)

            sum_data = 0
            for a in all:
                diff = abs(mktime(a.from_time.timetuple()) - mktime(a.through_time.timetuple()))
                convert_to_hour = diff / 3600
                sum_data = sum_data + convert_to_hour

            for a in all2:
                diff = abs(mktime(start_datetime.timetuple()) - mktime(a.through_time.timetuple()))
                convert_to_hour = diff / 3600
                sum_data = sum_data + convert_to_hour

            for a in all3:
                diff = abs(mktime(a.from_time.timetuple()) - mktime(end_datetime.timetuple()))
                convert_to_hour = diff / 3600
                sum_data = sum_data + convert_to_hour

            array_single.append(sum_data)

            start_datetime = datetime(
                year=start,
                month=10,
                day=1
            )

            end_datetime = datetime(
                year=start,
                month=12,
                day=31,
                hour=23,
                minute=59,
                second=59
            )

            all = Outage.objects.filter(from_time__range=(start_datetime, end_datetime),
                                        through_time__range=(start_datetime, end_datetime))
            all2 = Outage.objects.filter(from_time__lt=start_datetime,
                                         through_time__range=(start_datetime, end_datetime))
            all3 = Outage.objects.filter(from_time__range=(start_datetime, end_datetime),
                                         through_time__gt=end_datetime)

            sum_data = 0
            for a in all:
                diff = abs(mktime(a.from_time.timetuple()) - mktime(a.through_time.timetuple()))
                convert_to_hour = diff / 3600
                sum_data = sum_data + convert_to_hour

            for a in all2:
                diff = abs(mktime(start_datetime.timetuple()) - mktime(a.through_time.timetuple()))
                convert_to_hour = diff / 3600
                sum_data = sum_data + convert_to_hour

            for a in all3:
                diff = abs(mktime(a.from_time.timetuple()) - mktime(end_datetime.timetuple()))
                convert_to_hour = diff / 3600
                sum_data = sum_data + convert_to_hour

            array_single.append(sum_data)

            start = start + 1
        else:
            for i in range(12):

                if (i == 11):
                    number = abs((date(start, i + 1, 1) - date(start + 1, 1, 1)).days)

                else:
                    number = abs((date(start, i + 1, 1) - date(start, i + 2, 1)).days)
                start_datetime = datetime(
                    year=start,
                    month=i + 1,
                    day=1
                )

                end_datetime = datetime(
                    year=start,
                    month=i + 1,
                    day=number,
                    hour=23,
                    minute=59,
                    second=59
                )

                all = Outage.objects.filter(from_time__range=(start_datetime, end_datetime),
                                            through_time__range=(start_datetime, end_datetime))
                all2 = Outage.objects.filter(from_time__lt=start_datetime,
                                             through_time__range=(start_datetime, end_datetime))
                all3 = Outage.objects.filter(from_time__range=(start_datetime, end_datetime),
                                             through_time__gt=end_datetime)

                sum_data = 0
                for a in all:
                    diff = abs(mktime(a.from_time.timetuple()) - mktime(a.through_time.timetuple()))
                    convert_to_hour = diff / 3600
                    sum_data = sum_data + convert_to_hour

                for a in all2:
                    diff = abs(mktime(start_datetime.timetuple()) - mktime(a.through_time.timetuple()))
                    convert_to_hour = diff / 3600
                    sum_data = sum_data + convert_to_hour

                for a in all3:
                    diff = abs(mktime(a.from_time.timetuple()) - mktime(end_datetime.timetuple()))
                    convert_to_hour = diff / 3600
                    sum_data = sum_data + convert_to_hour

                array_single.append(sum_data)

            start = start + 1

    return array_single
