import pandas as pd
import plotly.express as px

from services.time_service import convert_time_to_decimal, convert_time_to_hrs
import constants as const

def sum_time_by_criteria(data, criteria):
    copy = data.copy()
    copy[const.time_in_decmial] = copy[const.time_in_decmial].astype(float)
    grouped_data = copy.groupby(criteria[0], as_index=False)    
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
    
def split_carryovers(data):
    # Split rows where start date and end date are different into 2 rows.
    # Day starts on 00:00:00 and ends on 23:59:59
    # 
    # Post condition: All rows will have same start and end date

    df = pd.DataFrame(columns=data.columns)

    for (_, row) in data.iterrows():
        end_of_day = pd.to_datetime("23:59:59", format="%H:%M:%S")
        start_of_day = pd.to_datetime("00:00:00", format="%H:%M:%S")

        start_date = pd.to_datetime(row[const.start_date], format="%d/%m/%Y")
        end_date = pd.to_datetime(row[const.end_date], format="%d/%m/%Y")

        if start_date.date() < end_date.date():
            start_time = pd.to_datetime(row[const.start_time], format="%H:%M:%S")
            end_time = pd.to_datetime(row[const.end_time], format="%H:%M:%S")

            split = row.copy()
            split[const.end_date] = row[const.start_date]
            split[const.end_time] = convert_time_to_hrs(end_of_day)
            delta = (end_of_day - start_time).components
            split[const.time_in_hours] = convert_time_to_hrs(delta)
            split[const.time_in_decmial] = convert_time_to_decimal(delta)

            row[const.start_date] = row[const.end_date]
            row[const.start_time] = convert_time_to_hrs(start_of_day)
            delta = (end_time - start_of_day).components
            row[const.time_in_hours] = convert_time_to_hrs(delta)
            row[const.time_in_decmial] = convert_time_to_decimal(delta)

            df = df.append(split)
        
        df = df.append(row)

    df.reset_index(drop=True, inplace=True)
    return df

def get_discret_colour_map(data):
    tags = data[const.tags].unique()

    # Supports 11 + 8 colours. Tags without colours are dropped
    colours = px.colors.qualitative.Prism + px.colors.qualitative.Safe
    return dict(zip(tags, colours))
    
