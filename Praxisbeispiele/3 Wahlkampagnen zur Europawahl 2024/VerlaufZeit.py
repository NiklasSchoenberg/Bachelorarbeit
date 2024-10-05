import pandas as pd
import matplotlib.pyplot as plt

file_path = 'Thesen/ParteienEUWahl/Kommentare.csv'
data = pd.read_csv(file_path)

keywords = ['']

keywords = [keyword.lower() for keyword in keywords]

data.columns = data.columns.str.strip()

data['Datum'] = pd.to_datetime(data['Datum'], format='%Y%m%d%H%M%S')

data['KommentarDEU'] = data['KommentarDEU'].str.lower()

end_date = '2024-06-09'
start_date = '2024-04-15'
data = data[(data['Datum'] >= start_date) & (data['Datum'] <= end_date)]

filtered_data = data[data['KommentarDEU'].str.contains('|'.join(keywords), case=False, na=False)]

filtered_data.set_index('Datum', inplace=True)

parteien = ['CDU', 'SPD', 'AFD', 'DieGruenen']

farben = {
    'CDU': 'tab:gray',
    'SPD': 'tab:red',
    'AFD': 'tab:blue',
    'DieGruenen': 'tab:green'
}

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 14))

for partei in parteien:
    partei_data = filtered_data[filtered_data['Partei'] == partei]
    
    daily_sentimentDE = partei_data['sentimentDEU'].resample('D').mean().dropna()
    daily_sentimentEN = partei_data['sentimentENG'].resample('D').mean().dropna()
    
    print(daily_sentimentEN.mean())
    
    ax1.plot(daily_sentimentDE.index, daily_sentimentDE, marker='x', linestyle='-', color=farben[partei], label=f'{partei} (DEU)')
    
    ax2.plot(daily_sentimentEN.index, daily_sentimentEN, marker='x', linestyle='-', color=farben[partei], label=f'{partei} (ENG)')

ax1.axhline(y=0, color='k', linestyle='--')
ax2.axhline(y=0, color='k', linestyle='--')

ax1.set_xlabel('Datum')
ax1.set_ylabel('Durchschnittliches Sentiment (DEU)')
ax1.set_ylim(-1, 1)
ax1.legend()
ax1.grid(True)

ax2.set_xlabel('Datum')
ax2.set_ylabel('Durchschnittliches Sentiment (ENG)')
ax2.set_ylim(-1, 1)
ax2.legend()
ax2.grid(True)

keywords_str = ', '.join(keywords)

fig.suptitle(f'Durchschnittliches Sentiment pro Tag für jede Partei')
fig.tight_layout(rect=[0, 0.03, 1, 0.97])
plt.show()
