import io
import base64
import pandas as pd

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

    # Address the issue where Clockify sometimes use "Tags" instead of "Tag" and 
    # "Duration (Decimal)"" instead of "Time (Decimal" as column headers
    columns_to_rename = {
        'Tags':'Tag', 
        'Duration (decimal)':'Time (decimal)', 
        'Duration (h)':'Time (h)'
    }
    df.rename(columns=columns_to_rename, inplace=True)
    return df
