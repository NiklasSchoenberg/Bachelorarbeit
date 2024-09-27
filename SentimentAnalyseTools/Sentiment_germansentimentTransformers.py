from transformers import pipeline

#https://huggingface.co/oliverguhr/german-sentiment-bert

pipe = pipeline("text-classification", model="oliverguhr/german-sentiment-bert", top_k=None)

def germansentimenttransformers(text):
    if not isinstance(text, str):
        return(None)
    result = pipe(text)[0]
    positive_score = 0
    negative_score = 0

    for label in result:
        if label['label'] == 'positive':
            positive_score = label['score']
        elif label['label'] == 'negative':
            negative_score = label['score']

    score_difference = positive_score - negative_score
    return(score_difference)
