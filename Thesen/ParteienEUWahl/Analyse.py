from pytube import extract
import pandas as pd
from instagrapi import Client
from tqdm import tqdm
import time
import csv
import os
import sys
ueberordner_pfad = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if ueberordner_pfad not in sys.path:
    sys.path.insert(0, ueberordner_pfad)
from SentimentAnalyseTools.Sentiment_twitter_roberta_base_sentiment_latest import twitterrobertabasesentiment
from SentimentAnalyseTools.Sentiment_German_Sentiment import german_sentiment
from uebersetzer import translation
import time
import csv
from tqdm import tqdm
from instagrapi import Client

commentList = []

# Instagram Client und Login-Funktion
def login():
    global cl
    cl = Client()
    cl.login('', '')


login()

def instagramcomments(url, quellenid, partei):
    try:
        media_id = cl.media_id(cl.media_pk_from_url(url))
        time.sleep(1)  # Kürzere Wartezeit für Tests, ggf. anpassen
        comments = cl.media_comments(media_id, 0)
        for comment in comments:
            if comment.replied_to_comment_id is None:
                text = comment.text
                commentList.append([
                    comment.pk,
                    quellenid,
                    'Instagram',
                    partei,
                    comment.created_at_utc,
                    len(text),
                    text
                ])
    except Exception as e:
        print(f"Fehler bei {url}: {e}")
        raise

quellen = []
with open("Thesen/ParteienEUWahl/Quellen.csv", 'r', newline='', encoding='utf-8') as liste:
    reader = csv.reader(liste)
    next(reader, None)  # Überspringt die Kopfzeile
    for zeile in reader:
        quellen.append((zeile[1], zeile[2]))


index = 0
while index < len(quellen):
    url, partei = quellen[index]
    try:
        instagramcomments(url, index + 1, partei)
        index += 1
    except Exception as e:
        print(f"Fehler bei {url}, warte 10 Minuten und versuche es erneut...")
        time.sleep(600)
        print("Erneuter Login...")
        login()


# Erstellen des DataFrames
data = pd.DataFrame(commentList, columns=['KommentarId', 'QuellenId', 'Plattform', 'Partei', 'Datum', 'Length', 'KommentarDEU'])

data.to_csv("Thesen/ParteienEUWahl/KommentareRAW.csv", index=False)

# Datumsspalte formatieren
data['Datum'] = pd.to_datetime(data['Datum'], utc=True, format='mixed').dt.strftime('%Y%m%d%H%M%S')

tqdm.pandas(desc="Übersetze Kommentare")
data['KommentarENG'] = data['KommentarDEU'].progress_apply(translation)
data['KommentarENG'].fillna(data['KommentarDEU'], inplace=True)

# Sentimentanalyse
tqdm.pandas(desc="Sentimentanalyse Deutsch")
data['sentimentDEU'] = data['KommentarDEU'].progress_apply(german_sentiment)

tqdm.pandas(desc="Sentimentanalyse Englisch")
data['KommentarENG'] = data['KommentarENG'].astype(str)
data['sentimentENG'] = data['KommentarENG'].progress_apply(twitterrobertabasesentiment)

# DataFrame speichern
data.to_csv("Thesen/ParteienEUWahl/KommentareAFD.csv", index=False)
print("Daten wurden erfolgreich gespeichert")

# Gesamtanzahl der Kommentare anzeigen
print(f"Gesamtanzahl der Kommentare: {len(data)}")