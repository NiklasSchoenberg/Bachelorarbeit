from pytube import extract
import pandas as pd
import googleapiclient.discovery
from instagrapi import Client
from bs4 import BeautifulSoup
from tqdm import tqdm
import requests
import csv
import os
import sys
ueberordner_pfad = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if ueberordner_pfad not in sys.path:
    sys.path.insert(0, ueberordner_pfad)
from Sentiment_twitter_roberta_base_sentiment_latest import twitterrobertabasesentiment
from Sentiment_German_Sentiment import german_sentiment
from uebersetzer import translation

commentList = []

#Youtube Kommentare
api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = ""

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey = DEVELOPER_KEY)

def load_comments(match, quellenid):
    for item in match["items"]:
        comment = item["snippet"]["topLevelComment"]["snippet"]
        text = comment["textDisplay"]
        commentList.append([
            item["id"],
            quellenid,
            'YouTube',
            comment["publishedAt"],
            len(text),
            text
        ])

def get_comment_threads(youtube, video_id, nextPageToken=None):
    results = youtube.commentThreads().list(
        part="snippet",
        maxResults=100,
        videoId = video_id,
        textFormat="plainText",
        pageToken=nextPageToken
    ).execute()
    return results

def youtubecomments(url, quellenid):
    video_id = extract.video_id(url)
    match = get_comment_threads(youtube, video_id)
    load_comments(match, quellenid)

    next_page_token = match.get("nextPageToken")
    while next_page_token:
        match = get_comment_threads(youtube, video_id, next_page_token)
        load_comments(match, quellenid)
        next_page_token = match.get("nextPageToken")

#Zeit Kommentare
def getuuid(url):
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")
    body_tag = soup.find("body")
    data_uuid = body_tag.get("data-uuid")
    return(data_uuid)

def zeitcomments(url, quellenid):
    data_uuid = getuuid(url)
    headers = {
        "accept": "*/*",
        "accept-language": "de,de-DE;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "origin": "https://www.zeit.de",
        "referer": "https://www.zeit.de/",
        r"^sec-ch-ua": "^^Microsoft",
        "sec-ch-ua-mobile": "?0",
        r"^sec-ch-ua-platform": "^^Windows^^^",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0"
    }

    ids=[]

    def seenids():
        seen_ids = ",".join(map(str, ids))
        return seen_ids

    root = "https://comments.zeit.de/comments/rpc/roots?uuid="+data_uuid+"&mode=newest"
    newroot = f"https://comments.zeit.de/comments/rpc/roots?uuid={data_uuid}&mode=newest&seen={{{seenids()}}}"

    while newroot != root:
            response = requests.get(newroot, headers=headers)
            data = response.json()
            for comment in data["comments"]:
                if comment["status"] not in ["deleted", "deleted_with_childs"]:
                    text = comment["content"]
                    soup= BeautifulSoup(text, "html.parser")
                    for blockquote in soup.find_all('blockquote'):
                        blockquote.decompose()
                    decoded_text = soup.get_text()
                    commentList.append([
                        comment["id"],
                        quellenid,
                        'ZeitOnline',
                        comment["created"],
                        len(decoded_text),
                        decoded_text
                    ]) 
                ids.append(comment["id"])
            root=newroot
            newroot= f"https://comments.zeit.de/comments/rpc/roots?uuid={data_uuid}&mode=newest&seen={{{seenids()}}}"

#Instagram Kommentare
cl = Client()
cl.login('','')
def instagramcomments(url, quellenid):
    media_id = cl.media_id(cl.media_pk_from_url(url))
    comments = cl.media_comments(media_id, 0)
    for comment in comments:
        if comment.replied_to_comment_id == None:
            text = comment.text
            commentList.append([
                comment.pk,
                quellenid,
                'Instagram',
                comment.created_at_utc,
                len(text),
                text
            ])


quellen = []
with open("Thesen/DeutschlandSpiele/Quellen.csv", 'r', newline='', encoding='utf-8') as liste:
    reader = csv.reader(liste)
    next(reader, None)
    for zeile in reader:
        # Füge die URL (zweite Spalte) zur Liste hinzu
        quellen.append(zeile[1])

for index, url in enumerate(tqdm(quellen, desc="Verarbeite Quellen"), start=1):
    if url.startswith("https://www.youtube"):
        youtubecomments(url, index)
    elif url.startswith("https://www.zeit"):
        zeitcomments(url, index)
    elif url.startswith("https://www.instagram"):
        instagramcomments(url, index)

# Erstellen des DataFrames
data = pd.DataFrame(commentList, columns=['KommentarId', 'QuellenId', 'Plattform', 'Datum', 'Length', 'KommentarDEU'])

# Datumsspalte einheitlich formatieren
data['Datum'] = pd.to_datetime(data['Datum'], utc=True, format='mixed').dt.strftime('%Y%m%d%H%M%S')

data.to_csv("Thesen/DeutschlandSpiele/KommentareRAW.csv", index=False)

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
data.to_csv("Thesen/DeutschlandSpiele/Kommentare.csv", index=False)
print("Daten wurden erfolgreich gespeichert")

# Gesamtanzahl der Kommentare anzeigen
print(f"Gesamtanzahl der Kommentare: {len(data)}")