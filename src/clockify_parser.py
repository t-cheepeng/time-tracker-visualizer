import collections
import csv
import io
import base64
import pandas as pd
from datetime import datetime 
from functools import reduce

def reduction(acc, nxt):
    if nxt[0] in acc:
        acc[nxt[0]] += nxt[1]
    else:
        acc[nxt[0]] = nxt[1]
    return acc


def date_tag_reduction(acc, nxt):
    weekday = datetime.strptime(nxt[0], "%d/%m/%Y").weekday()
    if weekday == 5 or weekday == 6:
        # Not a weekday
        weekend_dict = acc["weekend"]
        added = reduction(weekend_dict, (nxt[1], nxt[2]))
        acc["weekend"] = added
    else:
        # It's a weekday
        weekday_dict = acc["weekday"]
        added = reduction(weekday_dict, (nxt[1], nxt[2]))
        acc["weekday"] = added
    return acc

def extract_data():
    with open('..\\data\\clockify_report.csv', 'r') as f:
        data = csv.DictReader(f)
        acc_time_per_tag = reduce(reduction, map(lambda x: (
            x["Tag"], float(x["Time (decimal)"])), data), {})
        sorted_per_tag = collections.OrderedDict(sorted(acc_time_per_tag.items()))

    with open('..\\data\clockify_report_date_tag.csv', 'r') as f:
        data = csv.DictReader(f)
        acc_time_per_date = reduce(date_tag_reduction, map(lambda x: (
            x["Date"], x["Tag"], float(x["Time (decimal)"])), data), {"weekday": {}, "weekend": {}})
        sorted_weekday = collections.OrderedDict(
            sorted(acc_time_per_date["weekday"].items()))
        sorted_weekend = collections.OrderedDict(
            sorted(acc_time_per_date["weekend"].items()))
        sorted_per_date = {"weekday": sorted_weekday, "weekend": sorted_weekend}
        
    return {
        "averaged": sorted_per_tag,
        "weekday": sorted_per_date["weekday"],
        "weekend": sorted_per_date["weekend"]   
    }


def parse_data(content, filename):
    type, content_string = content.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        else:
            raise ValueError('Not a csv file')
    except Exception as e:
        print(e)
        return pd.DataFrame()

    return df
