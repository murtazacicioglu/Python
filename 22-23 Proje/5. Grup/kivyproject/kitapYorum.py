import requests
from bs4 import BeautifulSoup as BS

def yorumYap(user, password, comment, slug):
    user_data = {
        'username': user,
        'password': password,
        'comment': comment
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    }

    with requests.Session() as ses:
        url = "http://127.0.0.1:8000/hesap/mcomment/"+slug
        r = ses.get(url, headers=headers)
        soup = BS(r.content, "html5lib")
        user_data['csrfmiddlewaretoken'] = soup.find("input", attrs={"name": "csrfmiddlewaretoken"})["value"]
        yorum_yap = ses.post(url, headers=headers, data=user_data)
        
        if 'http://127.0.0.1:8000/' == yorum_yap.url:
            return True
        else:
            return False

