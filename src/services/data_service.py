import pandas as pd
import src.constants as const

def sum_time_by_criteria(data, criteria):
    # TODO Group by multiple criteria (is there even a need)
    grouped_data = data.groupby(criteria[0], as_index=False)
    return grouped_data[const.time_in_decmial].sum()

def sum_time(data):
    return data[const.time_in_decmial].sum()

def sum_time_by_workweek(data, sum_by_workweek):
    data['day'] = pd.to_datetime(data[const.start_date], format="%d/%m/%Y").dt.dayofweek
    if sum_by_workweek:
        data['day'] = (data['day'] < 5).astype(int)
    else:
        data['day'] = (data['day'] >= 5).astype(int)

    to_sum = data[data['day'] == 1]
    return sum_time_by_criteria(to_sum, [const.tags])
    

