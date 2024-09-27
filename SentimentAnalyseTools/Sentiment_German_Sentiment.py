import warnings
from transformers import pipeline

#https://huggingface.co/aari1995/German_Sentiment

pipe = pipeline(model="aari1995/German_Sentiment")

def german_sentiment(text):
    if not isinstance(text, str):
        return None

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=UserWarning)
    
        results = pipe(text, return_all_scores=True)[0]

        positive_score = 0
        negative_score = 0

        for label in results:
            if label['label'] == 'positive':
                positive_score = label['score']
            elif label['label'] == 'negative':
                negative_score = label['score']

        score_difference = positive_score - negative_score
        
        return score_difference
