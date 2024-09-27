import re
import matplotlib.pyplot as plt
import math
import numpy as np
from collections import Counter

tools = 9

# Die CSV-Datei einlesen und die Zeilen splitten
with open('KommentareToolScores.csv', 'r') as file:
    lines = file.readlines()

# Die Header extrahieren
header = lines[0].strip().split(',')

# Die Daten extrahieren
data = [line.strip().split(',') for line in lines[1:]]

header = header[-tools:]
data = [row[-tools:] for row in data]

num_charts = len(header)

# Subplots erstellen
fig, axes = plt.subplots(math.ceil(math.sqrt(tools)), math.ceil(math.sqrt(tools)), figsize=(20, 10))
axes = axes.flatten()

for col_idx in range(num_charts):
    col_values = []
    for row in data[-100:]:
        try:
            col_values.append(float(row[col_idx]))
        except ValueError:
            continue
    
    # Die Häufigkeit der Werte in 0,1er Schritten zählen
    bins = np.arange(-1, 1.01, 0.1)
    col_values_binned = np.digitize(col_values, bins) - 1
    frequency_count = Counter(col_values_binned)
    
    # Daten für X-Achse (Beschriftung von -10 bis 10 in 0,1er Schritten)
    x_values = bins[:-1] + 0.05
    y_frequency = [frequency_count[i] for i in range(len(bins)-1)]
    
    # Diagramm erstellen
    axes[col_idx].bar(x_values, y_frequency, width=0.1, align='center')
    
    # Achsenbeschriftungen setzen
    axes[col_idx].set_xlabel('Polarity-Scores')
    axes[col_idx].set_ylabel('Häufigkeit')
    
    # Titel setzen
    axes[col_idx].set_title(header[col_idx])
    
    # Y-Achse auf den Bereich von 0 bis max(y_frequency) setzen
    axes[col_idx].set_ylim(0, max(y_frequency, default=1))

# Platz für Achsenbeschriftungen und Titel schaffen
plt.tight_layout()
plt.show()