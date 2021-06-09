def convert_to_hrs_for_display(decimal_time, total_time):
    pct_of_day = decimal_time / total_time
    time_in_day = 24 * pct_of_day
    hours = int(time_in_day)
    minutes = (time_in_day * 60) % 60

    return "%dH:%02dm" % (hours, minutes)
