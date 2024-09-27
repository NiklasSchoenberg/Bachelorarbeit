from transformers import pipeline
import warnings

#https://huggingface.co/finiteautomata/bertweet-base-sentiment-analysis

pipe = pipeline("text-classification", model="finiteautomata/bertweet-base-sentiment-analysis", top_K=None)

def bertweetbasesentiment(text):
    if not isinstance(text, str):
        return None

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=UserWarning)
        
        pipe = pipeline(model="finiteautomata/bertweet-base-sentiment-analysis")

        results = pipe(text, return_all_scores=True)[0]

        positive_score = 0
        negative_score = 0

        for label in results:
            if label['label'] == 'POS':
                positive_score = label['score']
            elif label['label'] == 'NEG':
                negative_score = label['score']

        score_difference = positive_score - negative_score
        
        return score_difference