def sum_time_by_tag(data):
    return data.groupby('Tag', as_index=False)['Time (decimal)'].sum()

def sum_time(data):
    return data['Time (decimal)'].sum()

