import pandas as pd
import matplotlib.pyplot as plt

file_path = 'Thesen/IsraelGazaVerlauf/Kommentare.csv'
data = pd.read_csv(file_path)

data.columns = data.columns.str.strip()

data['Datum'] = pd.to_datetime(data['Datum'], format='%Y%m%d%H%M%S')

keywords = ['']

filtered_data = data[data['KommentarDEU'].str.contains('|'.join(keywords), case=False, na=False)]

filtered_data.set_index('Datum', inplace=True)
daily_sentimentDE = filtered_data['sentimentDEU'].resample('d').mean().dropna()
daily_sentimentEN = filtered_data['sentimentENG'].resample('d').mean().dropna()
daily_counts = filtered_data['sentimentENG'].resample('d').count().dropna()
print(daily_sentimentEN.mean())
print(daily_sentimentDE.mean())

fig, ax1 = plt.subplots(figsize=(14, 7))

color1 = 'tab:blue'
ax1.set_xlabel('Datum')
ax1.set_ylabel('Durchschnittliches Sentiment')
line1, = ax1.plot(daily_sentimentDE.index, daily_sentimentDE, marker='o', linestyle='-', color=color1, label='Deutsch')
ax1.tick_params(axis='y')
ax1.axhline(y=0, color='k', linestyle='--')
ax1.set_ylim(-1, 1)

ax2 = ax1.twinx()
line2, = ax2.plot(daily_sentimentEN.index, daily_sentimentEN, marker='o', linestyle='-', color='green', label='Englisch')
ax2.axhline(y=0, color='k', linestyle='--')
ax2.set_ylim(-1, 1)
ax2.get_yaxis().set_visible(False)

ax1.legend(handles=[line1, line2], loc='upper right', bbox_to_anchor=(1, 1), fontsize=14)

fig.suptitle(f'Durchschnittliches Sentiment pro Tag')
fig.tight_layout()
plt.grid(True)
plt.show()
