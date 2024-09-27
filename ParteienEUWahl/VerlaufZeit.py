import pandas as pd
import matplotlib.pyplot as plt

# CSV-Datei laden
file_path = 'Thesen/ParteienEUWahl/Kommentare.csv'
data = pd.read_csv(file_path)

keywords = ['']  # Fügen Sie hier Ihre Keywords ein

# Keywords in Kleinbuchstaben umwandeln
keywords = [keyword.lower() for keyword in keywords]

# Spaltennamen bereinigen (z.B. führende/nachfolgende Leerzeichen entfernen)
data.columns = data.columns.str.strip()

# Datumsspalte in ein Datetime-Format konvertieren
data['Datum'] = pd.to_datetime(data['Datum'], format='%Y%m%d%H%M%S')

# KommentarDEU in Kleinbuchstaben umwandeln
data['KommentarDEU'] = data['KommentarDEU'].str.lower()

# Filter auf Daten bis zum 09.06.2024
end_date = '2024-06-09'
start_date = '2024-04-15'
data = data[(data['Datum'] >= start_date) & (data['Datum'] <= end_date)]

# Filter auf Kommentare mit den Keywords
filtered_data = data[data['KommentarDEU'].str.contains('|'.join(keywords), case=False, na=False)]

# Daten nach Tag gruppieren und den durchschnittlichen Sentiment-Wert berechnen
filtered_data.set_index('Datum', inplace=True)

# Liste der Parteien
parteien = ['CDU', 'SPD', 'AFD', 'DieGruenen']

# Farben für die Parteien festlegen
farben = {
    'CDU': 'tab:gray',
    'SPD': 'tab:red',
    'AFD': 'tab:blue',
    'DieGruenen': 'tab:green'
}

# Erstellung der Subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 14))

for partei in parteien:
    # Daten für die aktuelle Partei filtern
    partei_data = filtered_data[filtered_data['Partei'] == partei]
    
    # Täglichen durchschnittlichen Sentiment berechnen
    daily_sentimentDE = partei_data['sentimentDEU'].resample('D').mean().dropna()
    daily_sentimentEN = partei_data['sentimentENG'].resample('D').mean().dropna()
    
    print(daily_sentimentEN.mean())
    
    # Durchschnittliches Sentiment Deutsch plotten
    ax1.plot(daily_sentimentDE.index, daily_sentimentDE, marker='x', linestyle='-', color=farben[partei], label=f'{partei} (DEU)')
    
    # Durchschnittliches Sentiment Englisch plotten
    ax2.plot(daily_sentimentEN.index, daily_sentimentEN, marker='x', linestyle='-', color=farben[partei], label=f'{partei} (ENG)')

# Null-Linie hinzufügen
ax1.axhline(y=0, color='k', linestyle='--')
ax2.axhline(y=0, color='k', linestyle='--')

# Erste Y-Achse beschriften
ax1.set_xlabel('Datum')
ax1.set_ylabel('Durchschnittliches Sentiment (DEU)')
ax1.set_ylim(-1, 1)
ax1.legend()
ax1.grid(True)

# Zweite Y-Achse beschriften
ax2.set_xlabel('Datum')
ax2.set_ylabel('Durchschnittliches Sentiment (ENG)')
ax2.set_ylim(-1, 1)
ax2.legend()
ax2.grid(True)

# Keywords in einen String zusammenfassen
keywords_str = ', '.join(keywords)

# Titel hinzufügen
fig.suptitle(f'Durchschnittliches Sentiment pro Tag für jede Partei')
fig.tight_layout(rect=[0, 0.03, 1, 0.97])
plt.show()

#\nKeywords: {keywords_str}