import requests
import os
from kivy.network.urlrequest import UrlRequest
from bs4 import BeautifulSoup

def on_success(req, result):
    soup = BeautifulSoup(result, "html.parser")
    img_tag = soup.find("img", {"class": "img-fluid rounded"})
    src = img_tag['src'] if img_tag else ""
    return src

def on_error(req, error):
    return ""

def get_image_src_from_url(url):
    req = UrlRequest(url, on_success=on_success, on_error=on_error)
    req.wait()

    src = on_success(req, req.result)
    return src

