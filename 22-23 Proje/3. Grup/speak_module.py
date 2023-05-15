#Bu kod, pyttsx3 kütüphanesini kullanarak metinleri sesli olarak okumak için tasarlanmıştır.
import pyttsx3 
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices') 
engine.setProperty('voice', voices[0].id)
def speak(text):
	engine.say(text)
	engine.runAndWait()



