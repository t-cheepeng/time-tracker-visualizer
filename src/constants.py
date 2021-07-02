# ============= DATA COLUMN NAMES =============
# Standardized names to be used for data. All lowercase letters with no spaces
project = 'project'
client = 'client'
desc = 'desc'
task = 'task'
user = 'user'
email = 'email'
tags = 'tags'
billable = 'billable'
start_date = 'startdate'
end_date = 'enddate'
start_time = 'starttime'
end_time = 'endtime'
time_in_hours = 'hours'
time_in_decmial = 'decimal'
bill_rate = 'br'
bill_amt = 'ba'

# ============= DATA COLUMN MAPPINGS =============
# Address the issue where Clockify sometimes use "Tags" instead of "Tag" and
# "Duration (Decimal)"" instead of "Time (Decimal" as column headers
#     'Tags':'Tag',
#     'Duration (decimal)':'Time (decimal)',
#     'Duration (h)':'Time (h)'
col_name_map = {
    'Project': project,
    'Client': client,
    'Description': desc,
    'Task': task,
    'User': user,
    'Email': email,
    'Tags': tags,
    'Tag': tags,
    'Billable': billable,
    'Start Date': start_date,
    'Start Time': start_time,
    'End Date': end_date,
    'End Time': end_time,
    'Time (h)': time_in_hours,
    'Duration (h)': time_in_hours,
    'Time (decmial)': time_in_decmial,
    'Duration (decimal)': time_in_decmial,
    'Billable Rate (SGD)': bill_rate,
    'Billable Amount (SGD)': bill_amt,
}

# TODO: Generate the list of dictionaries (below) automatically from the list of criteria
group_by_criteria = ['Tag', 'Description', 'Project', 'Client', 'User', 'Date', 'Task']
group_by_options = [
    {'label': 'Project', 'value': project},
    {'label': 'Client', 'value': client},
    {'label': 'User', 'value': user},
    {'label': 'Tag', 'value': tags},
    {'label': 'Date', 'value': start_date},
    {'label': 'Description', 'value': desc},
    {'label': 'Task', 'value': task},
]
