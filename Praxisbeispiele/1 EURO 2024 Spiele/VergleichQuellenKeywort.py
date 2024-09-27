import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Pfad zur CSV-Datei
csv_file_path = 'Thesen/EMSpiele/Kommentare.csv'

# CSV-Datei in ein DataFrame laden
df = pd.read_csv(csv_file_path)

df['KommentarDEU_lower'] = df['KommentarDEU'].str.lower()
df['KommentarENG_lower'] = df['KommentarENG'].str.lower()

def filter_by_keywords(df, keywords):
    keywords_lower = [keyword.lower() for keyword in keywords]
    keyword_filter = df['KommentarDEU_lower'].apply(lambda x: any(keyword in x for keyword in keywords_lower)) | \
                     df['KommentarENG_lower'].apply(lambda x: any(keyword in x for keyword in keywords_lower))
    return df[keyword_filter]

def durchschnittSentimentProQuellenDurchschnittSentimentAlleQuellen(df, keywords):
    filtered_df = filter_by_keywords(df, keywords)

    # Gruppierung nach QuellenId und Berechnung der Durchschnittswerte nur für die Sentiment-Spalten
    source_avg = filtered_df.groupby('QuellenId').agg({
        'sentimentDEU': 'mean',
        'sentimentENG': 'mean',
        'KommentarDEU_lower': 'count',  # Anzahl der deutschen Kommentare pro Quelle
        'KommentarENG_lower': 'count'   # Anzahl der englischen Kommentare pro Quelle
    })

    # Gesamtanzahl der Kommentare pro Quelle berechnen
    source_avg['AnzahlKommentareDEU'] = source_avg['KommentarDEU_lower']
    source_avg['AnzahlKommentareENG'] = source_avg['KommentarENG_lower']
    source_avg.drop(['KommentarDEU_lower', 'KommentarENG_lower'], axis=1, inplace=True)

    # Berechnung des Durchschnitts der Sentiments pro Quelle
    overall_avg_deu = source_avg['sentimentDEU'].mean()
    overall_avg_eng = source_avg['sentimentENG'].mean()

    source_avg['diffDEU'] = source_avg['sentimentDEU'] - overall_avg_deu
    source_avg['diffENG'] = source_avg['sentimentENG'] - overall_avg_eng

    # Plot erstellen
    bar_width = 0.35
    index = np.arange(len(source_avg))

    plt.figure(figsize=(12, 6))
    bar1 = plt.bar(index - bar_width/2, source_avg['diffDEU'], bar_width, label='Deutsch', color='skyblue')
    bar2 = plt.bar(index + bar_width/2, source_avg['diffENG'], bar_width, label='Englisch', color='lightgreen')

    plt.axhline(0, color='grey', linewidth=0.8)
    plt.xlabel('QuellenId')
    plt.ylabel('Differenz zum Gesamtdurchschnitt')
    plt.title('Differenz der durchschnittlichen Sentimentwerte von den einzelnen Quellen zum Gesamtdurchschnitt aller Quellen')
    plt.xticks(index, source_avg.index)
    plt.legend()

    # Anzahl der Kommentare pro Quelle über den Balken anzeigen (nur einmal pro Quelle)
    #for i, (deu_count, eng_count) in enumerate(zip(source_avg['AnzahlKommentareDEU'], source_avg['AnzahlKommentareENG'])):
    #    plt.text(i, max(source_avg['diffDEU'].max(), source_avg['diffENG'].max()) + 0.05, str(deu_count),
    #             color='black', fontweight='bold', ha='center', va='top')

    # Schlüsselwörter im Diagramm oben links anzeigen
    plt.text(-0.5, max(source_avg['diffDEU'].max(), source_avg['diffENG'].max()), f"Schlüsselwörter:\n{', '.join(keywords)}",
             verticalalignment='top', horizontalalignment='left', bbox=dict(facecolor='white', alpha=0.5))

    plt.show()

def durchschnittSentimentProQuellenDurchschnittSentimentAlleKommentare(df, keywords):
    filtered_df = filter_by_keywords(df, keywords)

    # Gruppierung nach QuellenId und Berechnung der Durchschnittswerte nur für die Sentiment-Spalten
    source_avg = filtered_df.groupby('QuellenId').agg({
        'sentimentDEU': 'mean',
        'sentimentENG': 'mean',
        'KommentarDEU_lower': 'count',  # Anzahl der deutschen Kommentare pro Quelle
        'KommentarENG_lower': 'count'   # Anzahl der englischen Kommentare pro Quelle
    })

    # Gesamtanzahl der Kommentare pro Quelle berechnen
    source_avg['AnzahlKommentareDEU'] = source_avg['KommentarDEU_lower']
    source_avg['AnzahlKommentareENG'] = source_avg['KommentarENG_lower']
    source_avg.drop(['KommentarDEU_lower', 'KommentarENG_lower'], axis=1, inplace=True)

    # Berechnung des Durchschnitts der Sentiments pro Quelle
    overall_avg_deu = filtered_df['sentimentDEU'].mean()
    overall_avg_eng = filtered_df['sentimentENG'].mean()

    source_avg['diffDEU'] = source_avg['sentimentDEU'] - overall_avg_deu
    source_avg['diffENG'] = source_avg['sentimentENG'] - overall_avg_eng

    # Plot erstellen
    bar_width = 0.35
    index = np.arange(len(source_avg))

    plt.figure(figsize=(12, 6))
    bar1 = plt.bar(index - bar_width/2, source_avg['diffDEU'], bar_width, label='Deutsch', color='skyblue')
    bar2 = plt.bar(index + bar_width/2, source_avg['diffENG'], bar_width, label='Englisch', color='lightgreen')

    plt.axhline(0, color='grey', linewidth=0.8)
    plt.xlabel('QuellenId')
    plt.ylabel('Differenz zum Gesamtdurchschnitt')
    plt.title('Differenz der durchschnittlichen Sentimentwerte von den einzelnen Quellen zum Gesamtdurchschnitt aller Kommentare')
    plt.xticks(index, source_avg.index)
    plt.legend()

    # Anzahl der Kommentare pro Quelle über den Balken anzeigen (nur einmal pro Quelle)
    for i, (deu_count, eng_count) in enumerate(zip(source_avg['AnzahlKommentareDEU'], source_avg['AnzahlKommentareENG'])):
        plt.text(i, max(source_avg['diffDEU'].max(), source_avg['diffENG'].max()) + 0.05, str(deu_count),
                 color='black', fontweight='bold', ha='center', va='top')

    # Schlüsselwörter im Diagramm oben links anzeigen
    plt.text(-0.5, max(source_avg['diffDEU'].max(), source_avg['diffENG'].max()), f"Schlüsselwörter:\n{', '.join(keywords)}",
             verticalalignment='top', horizontalalignment='left', bbox=dict(facecolor='white', alpha=0.5))
    plt.tight_layout()
    plt.show()

keywords = ['Schiedsrichter', 'Ref', 'Schiri', 'Unparteiischer', 'Unparteiische', 'Referee']
durchschnittSentimentProQuellenDurchschnittSentimentAlleQuellen(df, keywords)
durchschnittSentimentProQuellenDurchschnittSentimentAlleKommentare(df, keywords)