from textblob_de import TextBlobDE as TextBlob

#https://textblob-de.readthedocs.io/en/latest/

def textblobdesentiment(text):
    blob = TextBlob(text)
    return(blob.sentiment.polarity)