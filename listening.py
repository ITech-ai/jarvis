import speech_recognition as sr

r = sr.Recognizer()
mic = sr.Microphone()

print("Voice Recognition System Ready...")

def listen():
    try:
        with mic as source:
            r.adjust_for_ambient_noise(source, duration=0.5) 
            audio = r.listen(source, timeout=5, phrase_time_limit=8)

        text = r.recognize_google(audio, language="fa-IR")
        print(text)

        return text
    except:
        pass


