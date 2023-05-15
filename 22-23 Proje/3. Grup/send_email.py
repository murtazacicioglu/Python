import smtplib 
import urllib.request as urllib 

sender_email = "assistant.aibot@gmail.com"

def sending_mail(name, rec_email, message): 
    message = "Merhaba " + name + ',\n' + message 
    #MTP sunucusu ile bağlantı kurmak için smtplib.SMTP() işlevini kullanır.
    server = smtplib.SMTP('smtp.gmail.com', 587) 
    server.starttls() #SMTP sunucusu ile güvenli bir bağlantı oluşturur.

    server.login("assistant.aibot@gmail.com", "*******")
    print("Giriş Başarılı!")
    server.sendmail("Murtaza Hocam", rec_email, message)
    server.quit()
    return ("Başarılı bi şekilde gönderildi.. "+rec_email) 
