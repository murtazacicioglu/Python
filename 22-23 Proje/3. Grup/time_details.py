from datetime import datetime, date #tarih ile ilgili işlemler için kullanılır
def get_time(): #şu anki saat ve dakikayı %H hours %M minutes biçiminde bir dize olarak döndürür.
	now = datetime.now()
	current_time = now.strftime("%H saat %M dakika")
	return current_time

def get_hours(): #yalnızca saat bilgisini %H biçiminde bir dize olarak döndürür.
	now = datetime.now()
	return now.strftime("%H")

def get_date(): #şu anki tarihi %Y-%m-%d biçiminde bir dize olarak döndürür.
	return str(date.today())