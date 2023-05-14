import speech_recognition as sr  

r = sr.Recognizer()  

def listen():
    with sr.Microphone() as source:  
        print("Dinliyorum")  
        r.pause_threshold = 1 
        audio = r.listen(source)  
    query = ""  
    try:
        print("Tanınıyor..")
        query = r.recognize_google(audio, language='TR-tr')  
        print(f"Ben: {query}\n")  
    except:
        print("Lütfen tekrar eder misin...")  

    return query 
