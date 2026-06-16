import speech_recognition as sr

r = sr.Recognizer()
mic = sr.Microphone()

print("🎤 Speak...")

while True:
    with mic as source:
        audio = r.listen(source)

    text = r.recognize_google(audio, language="fa-IR")
    print("🧠:", text)