from datetime import datetime
import pandas as pd

file_path = 'Thesen/IsraelGazaVerlauf/Kommentare.csv'
df = pd.read_csv(file_path)
# Konvertiere die 'Datum'-Spalte in ein datetime-Format
df['Datum'] = pd.to_datetime(df['Datum'], format='%Y%m%d%H%M%S')

def count_comments_in_period(start_date, end_date):
    """
    Zählt die Anzahl der Kommentare, die innerhalb des angegebenen Zeitraums veröffentlicht wurden.
    
    :param start_date: Startdatum (im Format 'YYYY-MM-DD')
    :param end_date: Enddatum (im Format 'YYYY-MM-DD')
    :return: Anzahl der Kommentare im Zeitraum
    """
    # Konvertiere die Eingabedaten in datetime-Objekte
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Filtere die Kommentare, die innerhalb des Zeitraums veröffentlicht wurden
    filtered_comments = df[(df['Datum'] >= start_date) & (df['Datum'] <= end_date)]

    # Gib die Anzahl der gefilterten Kommentare zurück
    return filtered_comments.shape[0]

# Beispiel: Anzahl der Kommentare zwischen dem 1. Oktober 2023 und dem 7. Oktober 2023
print(count_comments_in_period('2023-10-18', '2023-10-19'))