import pandas as pd

csv_file_path = 'Thesen/EMSpiele/Kommentare.csv'

df = pd.read_csv(csv_file_path)

kommentare_pro_quellenid = df.groupby('QuellenId').size()

for quellen_id, anzahl in kommentare_pro_quellenid.items():
    print(f"QuellenId: {quellen_id}, Anzahl der Kommentare: {anzahl}")