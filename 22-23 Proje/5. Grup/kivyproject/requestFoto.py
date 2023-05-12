import requests
import os
from kivy.network.urlrequest import UrlRequest
from bs4 import BeautifulSoup


eski_dosya = "temp.png"

def resimYukle(url):
    if os.path.exists(eski_dosya):
        os.remove(eski_dosya)

    def on_success(req, result):
        with open(eski_dosya, "wb") as f:
            f.write(result)
        

    def on_error(req, error):
        
        return "Hatalı"

    req = UrlRequest(url, on_success=on_success, on_error=on_error)
    req.wait()

 


