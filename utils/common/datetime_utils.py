from datetime import datetime as dt

date_time_format = "%H:%M:%S %d.%m.%Y"


def int_to_date(value: int, to_string: bool = False):
    date = dt.fromtimestamp(value)

    return date.strftime(date_time_format) if to_string else date
