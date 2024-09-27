import pandas as pd
import matplotlib.pyplot as plt

# CSV-Datei laden
file_path = 'Thesen/IsraelGazaVerlauf/Kommentare.csv'
data = pd.read_csv(file_path)

# Spaltennamen bereinigen (z.B. führende/nachfolgende Leerzeichen entfernen)
data.columns = data.columns.str.strip()

# Datumsspalte in ein Datetime-Format konvertieren
data['Datum'] = pd.to_datetime(data['Datum'], format='%Y%m%d%H%M%S')

# Liste von Keywords, nach denen gefiltert werden soll
keywords = ['']  # Beispielhafte Liste von Keywords

# Filtern der Daten nach Kommentaren, die mindestens eines der Keywords enthalten
filtered_data = data[data['KommentarDEU'].str.contains('|'.join(keywords), case=False, na=False)]

# Daten nach Tag gruppieren und den durchschnittlichen Sentiment-Wert sowie die Anzahl der Kommentare berechnen
filtered_data.set_index('Datum', inplace=True)
daily_sentimentDE = filtered_data['sentimentDEU'].resample('d').mean().dropna()
daily_sentimentEN = filtered_data['sentimentENG'].resample('d').mean().dropna()
daily_counts = filtered_data['sentimentENG'].resample('d').count().dropna()
print(daily_sentimentEN.mean())
print(daily_sentimentDE.mean())

# Diagramm mit zwei Y-Achsen erstellen
fig, ax1 = plt.subplots(figsize=(14, 7))

# Erste Y-Achse: Durchschnittliches Sentiment Deutsch
color1 = 'tab:blue'
ax1.set_xlabel('Datum')
ax1.set_ylabel('Durchschnittliches Sentiment')
line1, = ax1.plot(daily_sentimentDE.index, daily_sentimentDE, marker='o', linestyle='-', color=color1, label='Deutsch')  # Legende hinzufügen
ax1.tick_params(axis='y')
ax1.axhline(y=0, color='k', linestyle='--')  # Null-Linie hinzufügen
ax1.set_ylim(-1, 1)

# Zweite Y-Achse: Durchschnittliches Sentiment Englisch
ax2 = ax1.twinx()
line2, = ax2.plot(daily_sentimentEN.index, daily_sentimentEN, marker='o', linestyle='-', color='green', label='Englisch')  # Legende hinzufügen
ax2.axhline(y=0, color='k', linestyle='--')  # Null-Linie hinzufügen
ax2.set_ylim(-1, 1)
ax2.get_yaxis().set_visible(False)  # Skala und Beschriftung der zweiten Y-Achse entfernen

# Legende innerhalb des Diagramms in der rechten oberen Ecke hinzufügen
ax1.legend(handles=[line1, line2], loc='upper right', bbox_to_anchor=(1, 1), fontsize=14)

# Titel und Gitter hinzufügen
fig.suptitle(f'Durchschnittliches Sentiment pro Tag')
fig.tight_layout()
plt.grid(True)
plt.show()
