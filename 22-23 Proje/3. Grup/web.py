import webbrowser
import os 

def open_google():
	webbrowser.open("https://google.com")

def open_youtube_song(song_name):
    query = song_name + " şarkısı"
    url = "https://www.youtube.com/results?search_query=" + query.replace(" ", "+")
    webbrowser.open(url)
    

def search_youtube(search):
    query = '+'.join(search.split())
    url = "https://www.youtube.com/results?search_query=" + query
    webbrowser.open(url)

def search_google(araştır):
    query = '+'.join(araştır.split())
    url = "https://www.google.com/search?q=" + query
    webbrowser.open(url)

def close_browser():
	os.system('pkill chrome')
