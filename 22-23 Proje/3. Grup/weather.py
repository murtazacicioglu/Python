import requests
from bs4 import BeautifulSoup
from colorama import Fore
import json

location = None

def get_location():
    global location
    if not location:
        print("Lokasyon bilgisi alınıyor...")
        send_url = 'http://api.ipstack.com/check?access_key=YOUR_ACCESS_KEY&output=json&legacy=1'
        r = requests.get(send_url)
        location = json.loads(r.text)
    return location

def check_weather(city=None):
    if not city:
        city = get_location()['city']
    country = get_location()['country_name']

    # Ülke Türkiye ise, hava durumunu Celsius olarak gösterir
    if country == 'Turkey':
        url = "https://www.mgm.gov.tr/tahmin/turkiye.aspx"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Şehir adının büyük harflerle ve Türkçe karakterleri düzeltme
        city = city.upper().replace("İ", "I")

        # Şehir adına uygun tahmin bölümünü bulma
        city_section = soup.find("td", string=city)
        if city_section:
            temperature = city_section.find_next("td").text.strip()
            description = city_section.find_next("td", class_="img-tur").find("img")['title']
            return "{COLOR}Hava Durumu: {TEMP}°C - {DESCR}{COLOR_RESET}".format(
                COLOR=Fore.BLUE, COLOR_RESET=Fore.RESET,
                TEMP=temperature, DESCR=description
            )
        else:
            return Fore.BLUE + "Şehir Bulunamadı" + Fore.RESET
    else:
        return "Bu hizmet yalnızca Türkiye için mevcuttur."
