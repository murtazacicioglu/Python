from kivy.network.urlrequest import UrlRequest
from bs4 import BeautifulSoup


def on_success(req, result):
    soup = BeautifulSoup(result, "html.parser")
    p_tag = soup.find("p", {"class": "card-text mt-1"})
    text = p_tag.text.strip() if p_tag else "Belirtilen etiket bulunamadı."
    return text

def on_error(req, error):
    return "No"

def get_text_from_url(url):
    req = UrlRequest(url, on_success=on_success, on_error=on_error)
    req.wait()

    text =on_success(req,req.result)
    return text


