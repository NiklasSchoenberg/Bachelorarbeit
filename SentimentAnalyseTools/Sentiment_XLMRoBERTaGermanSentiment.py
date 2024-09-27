from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

#https://huggingface.co/ssary/XLM-RoBERTa-German-sentiment

def xlmrobertagermansentiment(text):
    model = AutoModelForSequenceClassification.from_pretrained('ssary/XLM-RoBERTa-German-sentiment')
    tokenizer = AutoTokenizer.from_pretrained('ssary/XLM-RoBERTa-German-sentiment')
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
    numbers = predictions.tolist()[0]
    return(numbers[2]-numbers[0])