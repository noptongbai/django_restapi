def convert_humidity(humidity, quantity):
    if humidity == 0:
        return quantity
    else:
        convert = (100 - humidity) / 100.0
        return quantity * convert

