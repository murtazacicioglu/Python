from time_details import get_time, get_date  
from database import *
from input_module import take_input 
from output_module import output 
from internet import check_internet_connection, check_on_wikipedia
import assistant_details
from music import *
import os  
import random 
from web import open_google, close_browser, open_youtube_song, search_google, search_youtube 
import news
from weather import check_weather
import Calculator 
from location import get_location  
from send_email import sending_mail 
from AIBot import response 
from help_task import yardım 
#Kullanıcının sorgusunu işleyen işlev.
def  process(query):
	query = query.lower() 
	name = assistant_details.name
	query = query.replace(name, "") 
	noanswer = ["Üzgünüm,anlayamadım.", "Lütfen ayrıntılı açıklar mısınız?", "Anladığımdan emin değilim."]
	answer = None
	if len(query)<=1:
		return random.choice(noanswer)
	
	if query == "--yardım" or query == "--y":
		yardım(query)
		return "Senin için ne yapabilirim?"

	elif 'oynat' in query and 'müzik' not in query and 'şarkılar' not in query:
		answer = get_answer_from_memory("oynat")

	elif 'hava durumu' in query:
		answer = get_answer_from_memory("hava durumu")

	elif 'konum' in query: 
		answer = get_answer_from_memory("konum")

	elif 'araştır' in query: 
		answer = get_answer_from_memory("araştır")

	elif 'mail at' in query or 'mail at' in query: 
		answer = get_answer_from_memory("mail at")

	elif 'hesap makinesi' in query: 
		answer = get_answer_from_memory("hesap makinesi")

	elif 'harita' in query: 
		answer = get_answer_from_memory("google harita")	


	if answer == "zaman ayrıntılarını al":
		return ('Saat: '+ get_time())

	elif answer == "ad degistir":
		output("Tamam! Bana nasıl seslenmek istersin?")
		temp = take_input()
		if temp == assistant_details.name:
			return "Değistiremem. Sanırım eski adımdan memnunsun"
		else:
			update_name(temp)
			assistant_details.name = temp
			return "şimdi beni çağırabilirsin " + temp          

	elif answer == "tarihi söyle":
		return "Tarih  " + get_date()

	elif answer == "konuş":
		return turn_on_speech()

	elif answer == "konuşmayı durdur":
		return turn_off_speech()

	elif answer == "dinle":
		return turn_on_listen()
        
	elif answer == "dinlemeyi durdur":
		return turn_off_listen()

	elif answer == "google aç":
		open_google()
		return "google"

	elif answer == "tarayıcıyı kapat":
		close_browser()
		return "tarayıcı kapatılıyor"

	elif answer == "internet bağlantısını kontrol et":
		if check_internet_connection():
			return "internet bağlandı"
		else:
			return "internet bağlanmadı"

	elif answer == "müzik oynat":
		return play_music()

	elif answer == "müziği durdur":
		return pause_music()

	elif answer == "müziği kapat":
		return stop_music()

	elif answer == "sonraki şarkı":
		return next_song()

	elif answer == "önceki şarkı":
		return previous_song()

	elif answer == "oynat":
		müzik = play_specific_song(query)
		if "bulunamadı" in müzik:
			output("Müzik bulunamadı, Youtube'da araştırmanı önerebilirim!")
			res = take_input()
			if "yes" in res.lower():
				open_youtube_song(query.replace('oynat ', ''))
				return ("YouTube'da araştırılıyor")
			else:
				return ('Okay')
		else:
			return müzik
	
	elif answer == 'araştır':
		if 'youtube' in query:
			query = query.replace('araştır ','')
			query = query.replace('youtube da', '')
			search_youtube(query)
			return "Youtube'da araştır"
		else:
			query = query.replace('araştır ','')
			query = query.replace(' google', '')
			query = query.replace('google da', '')
			search_google(query)
			return "Google'da araştır"


	elif answer == "haberleri göster":
		return news.get_news()

	elif answer == "hava durumu":
		place = query.replace('hava durumu', '')
		return check_weather(place)

	elif answer == "konum":
		return get_location()

	elif answer == 'hesap makinesi':
		return Calculator(query)

	elif answer == "harita":
		indx = query.lower().split().index('harita')
		que = query.split()[indx + 1:]
		cmd =  'python map.py ' + ' '.join(que)
		os.system(cmd)
		return "Google haritalar açılıyor.."

	elif answer == "mail":
		name = query.replace("email at ", "")
		mail = get_emailId(name)
		if mail == '0':
			output("Email veritabanında bulunamadı, lütfen mail id'si giriniz")
			mail = take_input()
			insert_emailId(name, mail)
			output("Veri tabanına mail id'si eklendi")

		output("Enter message to send to "+name)
		msg = take_input()
		return sending_mail(name, mail, msg)

	else:
		res = response(query)
		if res != '0':
			return res
		
		else:
			output("Bunu bilmiyorum internette aramalı mıyım?")
			ans = take_input()
			if "yes" in ans:
				output("Wikipedia'da aranıyor...")
				answer = check_on_wikipedia(query)
				if answer != "":
					return answer
			else:
				output("Lütfen bunun ne anlama geldiğini söyleyebilir misiniz?")
				ans = take_input()
				if "şu anlama geliyor" in ans:
					ans = ans.replace("şu anlama geliyor", "")
					ans = ans.strip()

					value = get_answer_from_memory(ans)
					if value == "":
						return "Bu konuda yardımcı olamam"

					else:
						insert_question_and_answer(query, value)
						return "Teşekkürler, bir dahaki sefere hatırlayacağım"
				else:
					return "Bu konuda yardımcı olamam"
			return "Nothing"