def sum_time_by_tag(data):
    return data.groupby('Tags', as_index=False)['Duration (decimal)'].sum()

def sum_time(data):
    return data['Duration (decimal)'].sum()

