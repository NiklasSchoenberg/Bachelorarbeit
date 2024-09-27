import pandas as pd

# Lade den Umfragedatensatz und überspringe die zweite Zeile
df_umfrage = pd.read_csv('resultsfinal.csv', skiprows=[1])

# Wähle die letzten 100 Spalten aus
last_100_columns = df_umfrage.iloc[:, -100:]

# Konvertiere die ausgewählten Spalten in numerische Werte, Fehler ignorieren
last_100_columns = last_100_columns.apply(pd.to_numeric, errors='coerce')

# Berechne den Mittelwert jeder Spalte für diese Spalten
mean_values = last_100_columns.mean(axis=0)

# Berechne den minimalen und maximalen Wert und die Spannweite jeder Spalte
min_values = last_100_columns.min(axis=0) / 10
max_values = last_100_columns.max(axis=0) / 10
range_values = max_values - min_values

# Berechne die Varianz und Standardabweichung jeder Spalte
variance_values = last_100_columns.var(axis=0) / 10
std_dev_values = last_100_columns.std(axis=0) / 10
# Berechne den Median jeder Spalte
median_values = last_100_columns.median(axis=0) / 10

# Berechne das 25% und 75% Quantil jeder Spalte
quantile_25_values = last_100_columns.quantile(0.25, axis=0) / 10
quantile_75_values = last_100_columns.quantile(0.75, axis=0) / 10

# Teile die Kommentare in Sentiment-Bereiche ein
radius = 2.5
def get_sentiment(values):
    sentiments = []
    for value in values:
        if value < -radius:
            sentiments.append('negativ')
        elif value <= radius:
            sentiments.append('neutral')
        else:
            sentiments.append('positiv')
    return sentiments


# Lade die Text-CSV-Datei
df_text = pd.read_csv('KommentareBefragungStatistik.csv')

# Füge die berechneten Werte in die Spalten der Text-CSV-Datei ein
df_text['Mittelwert'] = mean_values.values
df_text['Min'] = min_values.values
df_text['Max'] = max_values.values
df_text['Spannweite'] = range_values.values
df_text['Varianz'] = variance_values.values
df_text['Standardabweichung'] = std_dev_values.values
df_text['Median'] = median_values.values
df_text['25Quantil'] = quantile_25_values.values
df_text['75Quantil'] = quantile_75_values.values
df_text['Sentiment'] = get_sentiment(mean_values.values)
# Speichere die aktualisierte Text-CSV-Datei
df_text.to_csv('KommentareBefragungStatistik.csv', index=False)

# Optional: Drucke das DataFrame aus, um das Ergebnis zu sehen
print(df_text)