from pandas._libs.tslibs.timestamps import Timestamp

def convert_to_hrs_for_display(decimal_time, total_time):
    pct_of_day = decimal_time / total_time
    time_in_day = 24 * pct_of_day
    hours = int(time_in_day)
    minutes = (time_in_day * 60) % 60

    return "%dH:%02dm" % (hours, minutes)

def convert_time_to_decimal(time):
    hours = 0
    minutes = 0
    seconds = 0

    if type(time) is Timestamp:
        (h, m, s) = time.time().split(":")
        hours = int(h)
        minutes = int(m)
        seconds = int(s)
    else:
        hours = time.hours
        minutes = time.minutes
        seconds = time.seconds

    decimal_time = hours + ((minutes * 60 + seconds) / 3600)
    return f'{decimal_time:.02f}'

def convert_time_to_hrs(time):
    if type(time) is Timestamp:
        return time.time()
    
    return f'{time.hours:02d}:{time.minutes:02d}:{time.seconds:02d}'
