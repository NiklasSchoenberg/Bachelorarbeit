import pandas as pd

# CSV-Datei einlesen
file_path = 'Thesen/IsraelGazaVerlauf/Kommentare.csv'
data = pd.read_csv(file_path)

# Funktion zur Zählung der positiven Werte in einer angegebenen Spalte
def count_positive_values(data, column_name):
    # Zählt die positiven Werte in der angegebenen Spalte
    positive_count = data[column_name][data[column_name] > 0].count()
    return positive_count

# Die Funktion aufrufen und das Ergebnis drucken
print(count_positive_values(data, 'sentimentDEU'))