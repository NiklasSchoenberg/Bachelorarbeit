import pandas as pd

csv_file_path = 'Thesen/DeutschlandSpiele/Kommentare.csv'

df = pd.read_csv(csv_file_path)

kommentare_pro_quellenid = df.groupby('Plattform').size()

for plattform, anzahl in kommentare_pro_quellenid.items():
    print(f"Plattform: {plattform}, Anzahl der Kommentare: {anzahl}")