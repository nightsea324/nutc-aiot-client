import pyttsx3
def tts(text):
    engine = pyttsx3.init()
    engine.setProperty('voice','zh')
    engine.say(text)        
    engine.runAndWait()

tts('前方號誌為')