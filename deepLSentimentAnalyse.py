from SentimentAnalyseTools.Sentiment_germansentimentTransformers import germansentimenttransformers
from SentimentAnalyseTools.Sentiment_German_Sentiment import german_sentiment
from SentimentAnalyseTools.Sentiment_textblob_de import textblobdesentiment
from SentimentAnalyseTools.Sentiment_NLTKVader import nltkvadersentiment
from SentimentAnalyseTools.Sentiment_spacy_Textblob import spacysentiment
from SentimentAnalyseTools.Sentiment_XLMRoBERTaGermanSentiment import xlmrobertagermansentiment
from SentimentAnalyseTools.Sentiment_distilbert_base_uncased_finetuned_sst_2_english import distilbertbasesentiment
from SentimentAnalyseTools.Sentiment_bertweet_base_sentiment_analysis import bertweetbasesentiment
from SentimentAnalyseTools.Sentiment_twitter_roberta_base_sentiment_latest import twitterrobertabasesentiment
from tqdm import tqdm

import pandas as pd

df=pd.read_csv('deepLKommentare.csv')
dfScores=pd.read_csv('deepLKommentareToolScores.csv')
tqdm.pandas(desc="Sentimentanalyse")
dfScores['Nummer'] = df['Nummer']
dfScores['germansentimenttransformers'] = df['Text'].progress_apply(germansentimenttransformers)
dfScores['german_sentiment'] = df['Text'].progress_apply(german_sentiment)
dfScores['xmlrobertagerman'] = df['Text'].progress_apply(xlmrobertagermansentiment)
dfScores['textblobde'] = df['Text'].progress_apply(textblobdesentiment)
dfScores['nltkvader'] = df['Englisch'].progress_apply(nltkvadersentiment)
dfScores['spacy'] = df['Englisch'].progress_apply(spacysentiment)
dfScores['distilbertbase'] = df['Englisch'].progress_apply(distilbertbasesentiment)
dfScores['bertweetbase'] = df['Englisch'].progress_apply(bertweetbasesentiment)
dfScores['twitterrobertabase'] = df['Englisch'].progress_apply(twitterrobertabasesentiment)

dfScores.to_csv('deepLKommentareToolScores.csv', index = False)