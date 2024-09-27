import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

# Pfad zur hochgeladenen Datei
file_path = 'Thesen/DeutschlandSpiele/Kommentare.csv'
data = pd.read_csv(file_path)

# Berechnung der Durchschnittswerte für sentimentDEU und sentimentENG
average_sentiments_deu = data.groupby('QuellenId')['sentimentDEU'].mean().reset_index()
average_sentiments_eng = data.groupby('QuellenId')['sentimentENG'].mean().reset_index()

# Festlegen der gewünschten Reihenfolge der Quellen
ordered_sources = [1, 5, 9, 2, 6, 10, 3, 7, 11, 4, 8, 12]

# Sortieren der Daten nach der gewünschten Reihenfolge für DEU
average_sentiments_deu['QuellenId'] = pd.Categorical(average_sentiments_deu['QuellenId'], categories=ordered_sources, ordered=True)
average_sentiments_deu = average_sentiments_deu.sort_values('QuellenId')

# Sortieren der Daten nach der gewünschten Reihenfolge für ENG
average_sentiments_eng['QuellenId'] = pd.Categorical(average_sentiments_eng['QuellenId'], categories=ordered_sources, ordered=True)
average_sentiments_eng = average_sentiments_eng.sort_values('QuellenId')

# Farbcodierung festlegen für DEU
colors_deu = ['blue' if q in [1, 2, 3, 4] else 'green' if q in [5, 6, 7, 8] else 'red' for q in average_sentiments_deu['QuellenId']]

# Farbcodierung festlegen für ENG
colors_eng = ['blue' if q in [1, 2, 3, 4] else 'green' if q in [5, 6, 7, 8] else 'red' for q in average_sentiments_eng['QuellenId']]

# Legend elements for platforms
legend_elements = [
    Patch(facecolor='blue', label='Zeit Online'),
    Patch(facecolor='green', label='Instagram'),
    Patch(facecolor='red', label='Youtube')
]

# Splitting the sources into 4 groups of 3
source_groups = [ordered_sources[i:i+3] for i in range(0, len(ordered_sources), 3)]
titles = ["Spiel 1", "Spiel 2", "Spiel 3", "Spiel 4"]

fig, axs = plt.subplots(2, 2, figsize=(20, 12))  # Creating a 2x2 grid for subplots

for i, ax in enumerate(axs.flatten()):
    group = source_groups[i]
    
    # Extracting the data for the current group
    deu_group = average_sentiments_deu[average_sentiments_deu['QuellenId'].isin(group)]
    eng_group = average_sentiments_eng[average_sentiments_eng['QuellenId'].isin(group)]
    
    # Getting the colors for the current group
    colors_deu_group = ['blue' if q in [1, 2, 3, 4] else 'green' if q in [5, 6, 7, 8] else 'red' for q in deu_group['QuellenId']]
    colors_eng_group = ['blue' if q in [1, 2, 3, 4] else 'green' if q in [5, 6, 7, 8] else 'red' for q in eng_group['QuellenId']]
    
    bar_width = 0.35
    index = np.arange(len(group))
    
    # Barplots für sentimentDEU
    ax.bar(index - bar_width/2, deu_group['sentimentDEU'], bar_width, label='sentimentDEU', color=colors_deu_group)
    
    # Barplots für sentimentENG
    ax.bar(index + bar_width/2, eng_group['sentimentENG'], bar_width, label='sentimentENG', color=colors_eng_group)
    
    # Diagramm-Einstellungen
    ax.set_xlabel('QuellenId')
    ax.set_ylabel('Durchschnittlicher Sentiment-Wert')
    ax.set_title(titles[i])
    ax.set_xticks(index)
    ax.set_xticklabels([str(q) for q in group])
    ax.set_ylim(-1, 1)

    # Anpassen der Legendenbeschriftungen
    ax.legend(handles=legend_elements, loc='upper left', title='Plattformen')

plt.tight_layout()
plt.show()