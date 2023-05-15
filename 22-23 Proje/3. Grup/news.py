import requests
from output_module import output
from internet import check_internet_connection   
def get_news(): 
    
    if check_internet_connection():
        # BBC news api 
        main_url = " https://newsapi.org/v1/articles?source=bbc-news&sortBy=top&apiKey=1bf3cdcaf711482589457e06c9936aef"
        open_bbc_page = requests.get(main_url).json() 
        article = open_bbc_page["articles"] 
        results = [] 
        for ar in article: 
            results.append(ar["title"]) 
        for i in range(len(results)): 
            print(str(i + 1) + " " + results[i])    

        return "Bugünün haberleri bu şekildeydi"
    else:
        return "Lütfen internet bağlantını kontrol et"