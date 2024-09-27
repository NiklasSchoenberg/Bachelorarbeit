import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('deepLKommentare.csv')

plt.figure(figsize=(10, 6))
plt.hist(df['laenge'], bins=30, edgecolor='black')
plt.title('Verteilung der Anzahl der Zeichen in der Spalte "Text"')
plt.xlabel('Anzahl der Zeichen')
plt.ylabel('Häufigkeit')
plt.grid(True)
plt.show()

df_sorted = df['laenge'].sort_values()
block_grenzen = np.array_split(df_sorted, 3)

grenzen = [block.iloc[-1] for block in block_grenzen]
print("Grenzen der drei Blöcke (in Zeichenanzahl):", grenzen)
