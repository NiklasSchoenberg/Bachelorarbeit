from deep_translator import GoogleTranslator
def translation(text):
    try:
        return GoogleTranslator(source='de', target='en').translate(text)
    except Exception as e:
        print(f"Translation error: {e}")
        return None