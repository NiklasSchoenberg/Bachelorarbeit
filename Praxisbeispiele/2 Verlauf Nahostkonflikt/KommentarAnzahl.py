from datetime import datetime
import pandas as pd

file_path = 'Thesen/IsraelGazaVerlauf/Kommentare.csv'
df = pd.read_csv(file_path)
df['Datum'] = pd.to_datetime(df['Datum'], format='%Y%m%d%H%M%S')

def count_comments_in_period(start_date, end_date):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)


    filtered_comments = df[(df['Datum'] >= start_date) & (df['Datum'] <= end_date)]

    return filtered_comments.shape[0]

print(count_comments_in_period('2023-10-18', '2023-10-19'))