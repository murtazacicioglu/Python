from kivy.network.urlrequest import UrlRequest
from bs4 import BeautifulSoup

def on_success(req, result):
    soup = BeautifulSoup(result, "html.parser")

    yorum_elem_list = soup.find_all("p", {"class": "mt-2"})
    yorum_list = [elem.text.strip() for elem in yorum_elem_list]

    return yorum_list

def on_error(req, error):
    return {"error": "No"}

def get_text_from_url(url):
    req = UrlRequest(url, on_success=on_success, on_error=on_error)
    req.wait()

    text =on_success(req,req.result)
    return text

