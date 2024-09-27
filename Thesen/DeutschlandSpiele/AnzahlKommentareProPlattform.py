import pandas as pd


# Pfad zur CSV-Datei
csv_file_path = 'Thesen/DeutschlandSpiele/Kommentare.csv'

# CSV-Datei in ein DataFrame laden
df = pd.read_csv(csv_file_path)

# Berechnen der Anzahl der Kommentare pro QuellenId
kommentare_pro_quellenid = df.groupby('Plattform').size()

# Ausgabe der Ergebnisse mit einer for-Schleife
for plattform, anzahl in kommentare_pro_quellenid.items():
    print(f"Plattform: {plattform}, Anzahl der Kommentare: {anzahl}")