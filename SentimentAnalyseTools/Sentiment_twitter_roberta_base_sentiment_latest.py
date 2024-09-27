import logging
from transformers import pipeline

#https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest

logging.getLogger("transformers").setLevel(logging.ERROR)

pipe = pipeline("text-classification", model="cardiffnlp/twitter-roberta-base-sentiment-latest", top_k=None)

def twitterrobertabasesentiment(text):
    if not isinstance(text, str):
        return None

    result = pipe(text)[0]
    
    positive_score = 0
    negative_score = 0

    for label in result:
        if label['label'] == 'positive':
            positive_score = label['score']
        elif label['label'] == 'negative':
            negative_score = label['score']

    score_difference = positive_score - negative_score
    return score_difference