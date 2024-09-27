import pandas as pd


# Pfad zur CSV-Datei
csv_file_path = 'Thesen/EMSpiele/Kommentare.csv'

# CSV-Datei in ein DataFrame laden
df = pd.read_csv(csv_file_path)

# Berechnen der Anzahl der Kommentare pro QuellenId
kommentare_pro_quellenid = df.groupby('QuellenId').size()

# Ausgabe der Ergebnisse mit einer for-Schleife
for quellen_id, anzahl in kommentare_pro_quellenid.items():
    print(f"QuellenId: {quellen_id}, Anzahl der Kommentare: {anzahl}")