import warnings
from transformers import pipeline

#https://huggingface.co/distilbert/distilbert-base-uncased-finetuned-sst-2-english

def distilbertbasesentiment(text):
    if not isinstance(text, str):
        return None

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=UserWarning)
        
        pipe = pipeline(model="distilbert-base-uncased-finetuned-sst-2-english")

        results = pipe(text, return_all_scores=True)[0]

        positive_score = 0
        negative_score = 0

        for label in results:
            if label['label'] == 'POSITIVE':
                positive_score = label['score']
            elif label['label'] == 'NEGATIVE':
                negative_score = label['score']

        score_difference = positive_score - negative_score
        
        return score_difference