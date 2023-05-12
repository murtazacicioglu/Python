import requests
from bs4 import BeautifulSoup
import re

def kitapKategori(url):
    response = requests.get(url)
    content = response.content

    soup = BeautifulSoup(content, 'html.parser')
    element = soup.find(class_="card-text")
    text = element.get_text()

    match = re.findall(r"(Kategori:[^<]+)", text)

    if match:
        kategoriler = [m.strip() for m in match]
        for kategori in kategoriler:
            return kategori.rstrip(",")
    else:
        return ["Belirtilmemiş"]

