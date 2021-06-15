def sum_time_by_criteria(data, criteria):
    # TODO Group by multiple criteria (is there even a need)
    grouped_data = data.groupby(criteria[0], as_index=False)
    return grouped_data['Time (decimal)'].sum()

def sum_time(data):
    return data['Time (decimal)'].sum()

