import csv
import matplotlib.pyplot as plt
import numpy as np

# Definieren Sie den Pfad zur CSV-Datei
csv_datei = 'resultsfinal.csv'

# Erstellen Sie ein Dictionary, um die Antworten für jede Frage zu speichern
antworten = {f'Q{i}_1': [] for i in range(1, 101)}

# Öffnen Sie die CSV-Datei und lesen Sie ihren Inhalt
with open(csv_datei, newline='', encoding='utf-8') as datei:
    leser = csv.DictReader(datei)
    
    # Iterieren Sie über jede Zeile in der CSV
    for zeile in leser:
        # Iterieren Sie über jede Frage und fügen Sie die letzten 28 Antworten der entsprechenden Liste hinzu
        for frage in antworten:
            # Extrahieren Sie die letzten 25 Werte und fügen Sie sie der Liste hinzu
            letzten_28_werte = [float(x) for x in zeile[frage].split(',')[-28:] if x.replace('.', '').replace('-', '').isdigit()]
            antworten[frage].extend(letzten_28_werte)

# Erstellen Sie Boxplots für jede Frage in einem Diagramm
plt.figure(figsize=(20, 10))

# Durchlaufen Sie das Dictionary und erstellen Sie für jede Frage einen Boxplot
for frage, ergebnisse in antworten.items():
    plt.boxplot(ergebnisse, positions=[int(frage.split('_')[0][1:])], widths=0.5)

    # Berechnen Sie den Mittelwert und fügen Sie ihn zum Plot hinzu
    mittelwert = np.mean(ergebnisse)
    plt.text(int(frage.split('_')[0][1:]), mittelwert, f'{mittelwert:.2f}', color='red', fontsize=8, ha='center')

plt.xlabel('Frage')
plt.ylabel('Sentiment')
plt.title('Boxplots für jede Frage')
plt.xticks(range(1, 101), [f'{i}' for i in range(1, 101)])
plt.yticks(np.arange(-10, 11, 1))  # Anpassen der Y-Achsen-Skala
plt.grid(True, axis='y')

# Diagramm anzeigen
plt.tight_layout()
plt.show()