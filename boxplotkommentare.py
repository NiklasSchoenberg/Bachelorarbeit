import csv
import matplotlib.pyplot as plt
import numpy as np

csv_datei = 'resultsfinal.csv'

antworten = {f'Q{i}_1': [] for i in range(1, 101)}

with open(csv_datei, newline='', encoding='utf-8') as datei:
    leser = csv.DictReader(datei)
    
    for zeile in leser:

        for frage in antworten:

            letzten_28_werte = [float(x) for x in zeile[frage].split(',')[-28:] if x.replace('.', '').replace('-', '').isdigit()]
            antworten[frage].extend(letzten_28_werte)

plt.figure(figsize=(20, 10))

for frage, ergebnisse in antworten.items():
    plt.boxplot(ergebnisse, positions=[int(frage.split('_')[0][1:])], widths=0.5)

    mittelwert = np.mean(ergebnisse)
    plt.text(int(frage.split('_')[0][1:]), mittelwert, f'{mittelwert:.2f}', color='red', fontsize=8, ha='center')

plt.xlabel('Frage')
plt.ylabel('Sentiment')
plt.title('Boxplots für jede Frage')
plt.xticks(range(1, 101), [f'{i}' for i in range(1, 101)])
plt.yticks(np.arange(-10, 11, 1))
plt.grid(True, axis='y')

plt.tight_layout()
plt.show()