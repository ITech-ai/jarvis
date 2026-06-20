from deep_translator import GoogleTranslator
def transletor(text , trans ="en"):
    if trans =="en":
        translated = GoogleTranslator(source='fa',target='en').translate(text)
    elif trans=="fa" :translated = GoogleTranslator(source='en',target='fa').translate(text)
    return translated
