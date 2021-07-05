import io
import base64
import pandas as pd
import json
from constants import col_name_map

def parse_data(content, filename):
    _, content_string = content.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        else:
            raise ValueError('Not a csv file')
    except Exception as e:
        print(e)
        return pd.DataFrame()

    df.rename(columns=col_name_map, inplace=True)
    return df

def parse_json_to_df(data):
    return pd.DataFrame.from_dict(json.loads(data))

def parse_df_to_json(df):
    return df.to_json()
