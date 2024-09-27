from nltk.sentiment.vader import SentimentIntensityAnalyzer

#https://www.nltk.org/_modules/nltk/sentiment/vader.html

sia = SentimentIntensityAnalyzer()
def nltkvadersentiment(text):
    sentimentScore = sia.polarity_scores(text)
    compound_score = sentimentScore['compound']
    return(compound_score)