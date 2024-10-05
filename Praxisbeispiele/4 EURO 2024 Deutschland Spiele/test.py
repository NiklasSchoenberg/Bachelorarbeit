import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

file_path = 'Thesen/DeutschlandSpiele/Kommentare.csv'
data = pd.read_csv(file_path)

average_sentiments_deu = data.groupby('QuellenId')['sentimentDEU'].mean().reset_index()
average_sentiments_eng = data.groupby('QuellenId')['sentimentENG'].mean().reset_index()

ordered_sources = [1, 5, 9, 2, 6, 10, 3, 7, 11, 4, 8, 12]

average_sentiments_deu['QuellenId'] = pd.Categorical(average_sentiments_deu['QuellenId'], categories=ordered_sources, ordered=True)
average_sentiments_deu = average_sentiments_deu.sort_values('QuellenId')

average_sentiments_eng['QuellenId'] = pd.Categorical(average_sentiments_eng['QuellenId'], categories=ordered_sources, ordered=True)
average_sentiments_eng = average_sentiments_eng.sort_values('QuellenId')

colors_deu = ['blue' if q in [1, 2, 3, 4] else 'green' if q in [5, 6, 7, 8] else 'red' for q in average_sentiments_deu['QuellenId']]

colors_eng = ['blue' if q in [1, 2, 3, 4] else 'green' if q in [5, 6, 7, 8] else 'red' for q in average_sentiments_eng['QuellenId']]

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

bar_width = 0.35
index = np.arange(len(ordered_sources))

bars_deu = ax1.bar(index, average_sentiments_deu['sentimentDEU'], bar_width, label='sentimentDEU', color=colors_deu)

bars_eng = ax2.bar(index, average_sentiments_eng['sentimentENG'], bar_width, label='sentimentENG', color=colors_eng)

legend_labels = {
    'blue': 'Zeit Online',
    'green': 'Instagram',
    'red': 'Youtube'
}

handles1, labels1 = ax1.get_legend_handles_labels()
unique_labels1 = list(set(labels1))
new_labels1 = [legend_labels.get(label, label) for label in unique_labels1]
ax1.legend(handles1, new_labels1, loc='upper right')

handles2, labels2 = ax2.get_legend_handles_labels()
unique_labels2 = list(set(labels2))
new_labels2 = [legend_labels.get(label, label) for label in unique_labels2]
ax2.legend(handles2, new_labels2, loc='upper right')

legend_elements = [
    Patch(facecolor='blue', label='Zeit Online'),
    Patch(facecolor='green', label='Instagram'),
    Patch(facecolor='red', label='Youtube')
]

ax1.legend(handles=legend_elements, loc='upper left', title='Plattformen')

ax1.set_ylabel('Durchschnittlicher Sentiment-Wert für DEU')
ax1.set_title('Vergleich der Sentiment-Werte für alle Quellen mit Beschriftung der Medien')
ax1.set_xticks(index)
ax1.set_xticklabels([str(q) for q in ordered_sources])

ax2.set_xlabel('QuellenId')
ax2.set_ylabel('Durchschnittlicher Sentiment-Wert für ENG')
ax2.set_xticks(index)
ax2.set_xticklabels([str(q) for q in ordered_sources])

plt.tight_layout()
plt.show()
