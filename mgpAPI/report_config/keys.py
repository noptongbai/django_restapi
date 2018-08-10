from rest_framework import serializers

from TLC import tlc
from TWC import twc
from TWQ import twq
from TLQ import tlq
from ME import me
from MG import mg
from MS import ms
from PC import pc
from PQ import pq
from O import o
from OU import ou
from OP import op
from OV import ov


def create_data(data):
    array_sum = []
    year = data["year"]
    history = data["history"]
    period = data["period"]

    range_date = return_period_type_toint(period)

    start = int(year) - int(history)
    end = int(year) + 1

    for k in data.getlist("keys"):
        array_single = return_key(k, range_date, start, end)
        array_sum.append(array_single)
    return array_sum


def return_period_type_toint(period):
    if period == "Month":
        return 1
    elif period == "Quarter":
        return 3
    else:
        return 12


def return_key(data, range_date, start, end):
    print "test"
    if "PQ" in data:
        array_single = pq(data, range_date, start, end)
        return array_single
    elif "PC" in data:
        array_single = pc(data, range_date, start, end)
        return array_single
    elif "TLQ" in data:
        array_single = tlq(data, range_date, start, end)
        return array_single

    elif "TLC" in data:
        array_single = tlc(data, range_date, start, end)
        return array_single

    elif "TWQ" in data:
        array_single = twq(data, range_date, start, end)
        return array_single
    elif "TWC" in data:
        array_single = twc(data, range_date, start, end)
        return array_single
    elif "MG" in data:
        array_single = mg(data, range_date, start, end)
        return array_single
    elif "ME" in data:
        array_single = me(data, range_date, start, end)
        return array_single
    elif "MS" in data:
        array_single = ms(data, range_date, start, end)
        return array_single
    elif "OV" in data:
        array_single = ov(data, range_date, start, end)
        return array_single
    elif "OP" in data:
        array_single = op(data, range_date, start, end)
        return array_single
    elif "OU" in data:
        array_single = ou(data, range_date, start, end)
        return array_single
    elif "O" in data:
        array_single = o(data, range_date, start, end)
        return array_single
    else:
        raise serializers.ValidationError({"error": "not found this keys"})
