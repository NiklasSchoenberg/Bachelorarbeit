import pandas as pd

# CSV-Dateien lesen
df1 = pd.read_csv('Thesen/ParteienEUWahl/KommentareCDU.csv')
df2 = pd.read_csv('Thesen/ParteienEUWahl/KommentareSPD.csv')
df3 = pd.read_csv('Thesen/ParteienEUWahl/KommentareDIEGRUENEN.csv')
df4 = pd.read_csv('Thesen/ParteienEUWahl/KommentareAFD.csv')

# Zusammenführen der Datenframes basierend auf einer gemeinsamen Spalte (z.B. 'ID')
df_merged = pd.concat([df1, df2, df3, df4], ignore_index=True)

# Die zusammengeführte CSV-Datei speichern
df_merged.to_csv('Thesen/ParteienEUWahl/Kommentare.csv', index=False)