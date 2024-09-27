import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Pfad zur CSV-Datei
csv_file_path = 'Thesen/EMSpiele/Kommentare.csv'

# CSV-Datei in ein DataFrame laden
df = pd.read_csv(csv_file_path)

def durchschnittSentimentProQuellenDurchschnittSentimentAlleQuellen(df):
    # Berechnung des Durchschnitts pro Quelle
    source_avg = df.groupby('QuellenId')[['sentimentDEU', 'sentimentENG']].mean()
    
    # Berechnung des Gesamtdurchschnitts aus den Quellen-Durchschnittswerten
    overall_avg_deu = source_avg['sentimentDEU'].mean()
    overall_avg_eng = source_avg['sentimentENG'].mean()

    # Berechnung der Differenzen der Quellen-Durchschnittswerte zum Gesamtdurchschnitt
    source_avg['diffDEU'] = source_avg['sentimentDEU'] - overall_avg_deu
    source_avg['diffENG'] = source_avg['sentimentENG'] - overall_avg_eng

    # Plot erstellen
    bar_width = 0.35
    index = np.arange(len(source_avg))

    plt.figure(figsize=(12, 6))
    bar1 = plt.bar(index, source_avg['diffDEU'], bar_width, label='Deutsch', color='skyblue')
    bar2 = plt.bar(index + bar_width, source_avg['diffENG'], bar_width, label='Englisch', color='lightgreen')

    plt.axhline(0, color='grey', linewidth=0.8)
    plt.xlabel('QuellenId')
    plt.ylabel('Differenz zum Gesamtdurchschnitt')
    plt.title('Differenz der durchschnittlichen Sentimentwerte von den einzelnen Quellen zum Gesamtdurchschnitt aller Quellen')
    plt.xticks(index + bar_width / 2, source_avg.index)
    plt.legend()

    plt.show()

def durchschnittSentimentProQuellenDurchschnittSentimentAlleKommentare(df):
    # Berechnung der Durchschnittswerte
    overall_avg_deu = df['sentimentDEU'].mean()
    overall_avg_eng = df['sentimentENG'].mean()

    # Gruppierung nach QuellenId und Berechnung der Durchschnittswerte nur für die Sentiment-Spalten
    source_avg = df.groupby('QuellenId')[['sentimentDEU', 'sentimentENG']].mean()
    source_avg['diffDEU'] = source_avg['sentimentDEU'] - overall_avg_deu
    source_avg['diffENG'] = source_avg['sentimentENG'] - overall_avg_eng

    # Plot erstellen
    bar_width = 0.35
    index = np.arange(len(source_avg))

    plt.figure(figsize=(12, 6))
    bar1 = plt.bar(index, source_avg['diffDEU'], bar_width, label='Deutsch', color='skyblue')
    bar2 = plt.bar(index + bar_width, source_avg['diffENG'], bar_width, label='Englisch', color='lightgreen')

    plt.axhline(0, color='grey', linewidth=0.8)
    plt.xlabel('QuellenId')
    plt.ylabel('Differenz zum Gesamtdurchschnitt')
    plt.title('Differenz der durchschnittlichen Sentimentwerte von den einzelnen Quellen zum Gesamtdurchschnitt aller Kommentare')
    plt.xticks(index + bar_width / 2, source_avg.index)
    plt.legend()

    plt.show()

# Aufruf der Methoden
durchschnittSentimentProQuellenDurchschnittSentimentAlleQuellen(df)

durchschnittSentimentProQuellenDurchschnittSentimentAlleKommentare(df)