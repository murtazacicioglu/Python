import urllib.request  
import wikipedia 

def check_internet_connection():
    try:
        urllib.request.urlopen('http://google.com')  
        return True 
    except:
        return False 

def check_on_wikipedia(query):
    query = query.lower() 

    query = query.replace("Kim", "") 
    query = query.replace("Ne", "")  
    query = query.replace("Kim biliyor musun?", "") 
    query = query.replace("Bana anlat ", "") 

    query = query.strip() 

    try:
        veri = wikipedia.summary(query, sentences=2) 
        veri = "Wikipedia'ya göre " + veri  
        return veri 
    except Exception as e:
        return ""

