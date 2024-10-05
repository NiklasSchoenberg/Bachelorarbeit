import pandas as pd

df_umfrage = pd.read_csv('resultsfinal.csv', skiprows=[1])

last_100_columns = df_umfrage.iloc[:, -100:]

last_100_columns = last_100_columns.apply(pd.to_numeric, errors='coerce')

mean_values = last_100_columns.mean(axis=0)

min_values = last_100_columns.min(axis=0) / 10
max_values = last_100_columns.max(axis=0) / 10
range_values = max_values - min_values

variance_values = last_100_columns.var(axis=0) / 10
std_dev_values = last_100_columns.std(axis=0) / 10

median_values = last_100_columns.median(axis=0) / 10

quantile_25_values = last_100_columns.quantile(0.25, axis=0) / 10
quantile_75_values = last_100_columns.quantile(0.75, axis=0) / 10

radius = 2.5
def get_sentiment(values):
    sentiments = []
    for value in values:
        if value < -radius:
            sentiments.append('negativ')
        elif value <= radius:
            sentiments.append('neutral')
        else:
            sentiments.append('positiv')
    return sentiments


df_text = pd.read_csv('KommentareBefragungStatistik.csv')

df_text['Mittelwert'] = mean_values.values
df_text['Min'] = min_values.values
df_text['Max'] = max_values.values
df_text['Spannweite'] = range_values.values
df_text['Varianz'] = variance_values.values
df_text['Standardabweichung'] = std_dev_values.values
df_text['Median'] = median_values.values
df_text['25Quantil'] = quantile_25_values.values
df_text['75Quantil'] = quantile_75_values.values
df_text['Sentiment'] = get_sentiment(mean_values.values)

df_text.to_csv('KommentareBefragungStatistik.csv', index=False)

print(df_text)