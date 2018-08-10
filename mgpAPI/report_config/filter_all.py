def filter_all(data):
    year = data["year"]
    history = data["history"]
    period = data["period"]

    if int(history) == 0:
        period_array = return_period_type(period)
        if period_array == []:
            period_array.append(year)
            return period_array
        else:
            period_array2 = []
            for a in period_array:
                a = a + year
                period_array2.append(a)
            return period_array2
    else:
        year_int = int(year)
        history_int = int(history)
        year_int = year_int - history_int
        ref = 0
        period_array = return_period_type(period)
        period_array2 = []
        while ref != history_int + 1:
            if period == "Month" or period == "Quarter":
                for a in period_array:
                    a = a + (str(year_int))
                    period_array2.append(a)
            else:
                period_array2.append(str(year_int))
            ref = ref + 1
            year_int = year_int + 1
        return period_array2
    # for a in data.getlist('keys'):
    #     print a
    return []


def return_period_type(period):
    if period == "Month":
        return ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct',
                'Nov', 'Dec']
    elif period == "Quarter":
        return ['Q1', 'Q2','Q3','Q4']
    else:
        return []
