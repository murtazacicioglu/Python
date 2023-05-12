from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton, MDRaisedButton, MDRoundFlatButton
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivymd.uix.label import MDLabel
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.camera import Camera
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.properties import ObjectProperty
from kivy.clock import Clock
import pytesseract
import csv
import cv2
import os
import requestOlayi
import requestYorum
import requestFoto
import requestFotoUrl
import requestKategori
import hesapGiris
import kitapYorum
from slugify import slugify




class HomePage(Screen):
    def giris(self):
        kullaniciAdi = self.ids.welcome_label.text = "Giriş Yapılıyor"
        sifre = self.ids.user.text = ""
        self.ids.password.text = ""

        yorum_yap_screen = MyApp.get_running_app().root.get_screen('YorumYap')
        yorum_yap_screen.kullaniciAdi = kullaniciAdi
        yorum_yap_screen.sifre = sifre

        Clock.schedule_once(lambda dt: setattr(self.manager, 'current', 'LoginWindow'), 1)

    def logger(self):
        kullaniciAdi = self.ids.user.text
        kullaniciAdi = kullaniciAdi.strip()
        sifre = self.ids.password.text
        sifre = sifre.strip()
        statueBool = hesapGiris.hesapVarMi(kullaniciAdi, sifre)

        if statueBool:
            self.ids.welcome_label.text = "Giriş Yapılıyor"
            Clock.schedule_once(lambda dt: setattr(self.manager, 'current', 'LoginWindow'), 1)
            
            yorum_yap_screen = MyApp.get_running_app().root.get_screen('YorumYap')
            
            yorum_yap_screen.kullaniciAdi = kullaniciAdi
            yorum_yap_screen.sifre = sifre

            self.kullaniciAdi = ""
            self.sifre = ""
        else:
            self.ids.welcome_label.text = "Hatalı Giriş"

class YorumYap(Screen):
    kullaniciAdi = ""
    sifre = ""
    slug = "kuyucakl-yusuf"

    def yorumYaz(self):
        yorum = self.ids.yorum.text
        
        self.kullaniciAdi
        self.sifre
        self.slug
        statueBool = kitapYorum.yorumYap(self.kullaniciAdi, self.sifre, yorum, self.slug)

        if statueBool:
            self.ids.yorum.text = ""
            popup = Popup(title="Başarılı", content=Label(text="Mesajınız başarılı bir şekilde gönderildi."), size_hint=(None, None), size=(400, 200))
            popup.open()
        else:
            popup = Popup(title="Başarısız", content=Label(text="Mesajınız gönderilemedi.Lütfen hesabınıza giriş yapınız"), size_hint=(None, None), size=(400, 200))
            popup.open()

    
    def geriDon(self):
        self.ids.yorum.text = ""
        self.manager.current = "Comments"
        

class Hakkimizda(Screen):
    pass
        
class BookWindow(Screen):
    
    def yorumSayfasi(self):
        pass
    
        
class Comments(Screen):
    
    
    def goBack(self):
        self.manager.current = "BookWindow"


class LoginWindow(Screen):
    TR2ENG = str.maketrans("çğıöşü","cgiosu")

    def find_book(self, text):
        with open("books2.csv", newline="", encoding="ANSI") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            for row in reader:
                if text.casefold() in row[2].casefold() or text.casefold() in row[2].translate(self.TR2ENG).casefold() or text.casefold() in row[2].translate(self.TR2ENG).casefold().replace(" ","") or row[2].translate(self.TR2ENG).casefold().replace(" ","") in text.casefold():
                    return (row[2], row[10])
            return None
    
    def set_list(self, text=""):

        self.ids.container.clear_widgets()
        with open("books2.csv", newline="", encoding="ANSI") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            count = 0  
            for row in reader:

                if row[2].casefold().startswith(text.casefold()) or row[2].translate(self.TR2ENG).casefold().startswith(text.casefold()):
                    self.ids.container.add_widget(
                        OneLineListItem(text=row[2],on_press=lambda x, name=row[2] ,yazar = row[10]: self.pressed(name,yazar))
                    )
                    count += 1
                    if count >= 10:
                        break
    

    def pressed(self,kitapAdi,yazarAdi):
        
        book_window = self.manager.get_screen("BookWindow")
        book_window.ids.kitaplar.title = kitapAdi
        book_window.ids.yazar.text = "Yazar Adı: " + yazarAdi
        book_window.ids.yazar.markup = True
        
        urlSon = kitapAdi.replace("ı","")
        urlSon = slugify(urlSon)

        yorum_yap_screen = MyApp.get_running_app().root.get_screen('YorumYap')
        yorum_yap_screen.slug = urlSon

        kitapAciklama = "http://127.0.0.1:8000/kutuphane/"+urlSon
        book_window.ids.aciklama.text = requestOlayi.get_text_from_url(kitapAciklama)
        book_window.ids.kategori.text = requestKategori.kitapKategori(kitapAciklama)

        kitapFotoURL = requestFotoUrl.get_image_src_from_url(kitapAciklama)
        requestFoto.resimYukle("http://127.0.0.1:8000"+kitapFotoURL)
        book_window.ids.kitapResim.source = "temp.png"
        book_window.ids.kitapResim.reload()
        
        comments_samp = self.manager.get_screen("Comments")
        comments_samp.ids.yorumBaslik.title = kitapAdi

        yorum_list = requestYorum.get_text_from_url(kitapAciklama) 

        for i in range(0, len(yorum_list), 2):
            yorumlar_listesi = MDBoxLayout(orientation="horizontal", size_hint_y=None, height="48dp")
            yorumlar_listesi.add_widget(MDIconButton(icon="comment-account"))
            yorumlar_listesi.add_widget(MDLabel(text=yorum_list[i], halign="center", font_style="Subtitle2"))
            yorumlar_listesi.add_widget(MDLabel(text=yorum_list[i+1], halign="center", font_style="Subtitle2"))
            comments_samp.ids.yorumlar.add_widget(yorumlar_listesi)

        self.manager.current = "BookWindow"

    
    def goBack(self):
        comments_samp = self.manager.get_screen("Comments")
        comments_samp.ids.yorumlar.clear_widgets()
        self.manager.current = "LoginWindow"



class FirstWindow(Screen):
    
    def calisKamera(self):

        self.remove_widget(self.ids.kameraAc)
        self.remove_widget(self.ids.geriDon)

        self.camera = Camera(resolution=(1920, 1080), play=True)
        self.camera.size_hint = (1, 1)
        self.camera.pos_hint = {"center_x":0.5,"y":0.7}


        self.buttonPhoto = MDRoundFlatButton(text="Fotoğraf Çek")
        self.buttonPhoto.size_hint = (0.2, 0.2)
        self.buttonPhoto.radius = "15dp"
        self.buttonPhoto.pos_hint = {'center_x': 0.5, 'y': 0.1}
        self.buttonPhoto.bind(on_press=self.take_picture)

        self.buttonGeri = MDRoundFlatButton(text="Geri")
        self.buttonGeri.size_hint = (0.2, 0.2)
        self.buttonGeri.radius = "15dp"
        self.buttonGeri.pos_hint = {'x': 0.4, 'y': 0.1}
        self.buttonGeri.bind(on_press=self.kameraDur)

        self.text_output = Label(text="",color= (0,0,0,1))
        self.text_output.pos_hint = {"x":0,"y":0}

        self.ids.kameraArayuz.add_widget(self.camera)
        self.ids.kameraArayuz.add_widget(self.buttonPhoto)
        self.ids.kameraArayuz.add_widget(self.buttonGeri)
        self.ids.kameraArayuz.add_widget(self.text_output)
        self.camera.play        

    def take_picture(self, *args):
        if not self.camera.play:
            self.camera.play = True
        os.environ['TESSDATA_PREFIX'] = 'C:/Program Files/Tesseract-OCR/tessdata'
        img = self.camera.export_as_image()
        img.save("photo.png")
        img = cv2.imread("photo.png")

        kitap = pytesseract.image_to_string(img, lang="tur")

        if kitap:
            login_window = self.manager.get_screen("LoginWindow")
            TR2ENG = str.maketrans("çğıöşü","cgiosu")

            new_text = kitap.replace(" ","")
            new_text = new_text.replace("|","")
            new_text = new_text.replace("/","")
            new_text = new_text.replace("\n","")
            new_text = new_text.lower()
            new_text = new_text.translate(TR2ENG)

            print(new_text)

            self.manager.get_screen("LoginWindow")
            kitapSonuclar =login_window.find_book(text=new_text)

            if kitapSonuclar != None:
                login_window.pressed(kitapSonuclar[0],kitapSonuclar[1])
                self.text_output.text = ""

            else:
                self.text_output.text = "Böyle bir kitap bulunamadı..."

    def kameraDur(self,instance):
        self.camera.play = False
        self.manager.current = "LoginWindow"




class MyApp(MDApp):

    def build(self):
        sm = ScreenManager()
        self.theme_cls.primary_palette = "BlueGray"

        Builder.load_file("main.kv") 

        sm.add_widget(HomePage(name="HomePage"))
        sm.add_widget(Hakkimizda(name="Hakkimizda"))
        sm.add_widget(YorumYap(name="YorumYap"))
        sm.add_widget(LoginWindow(name="LoginWindow"))
        sm.add_widget(FirstWindow(name="FirstWindow"))
        sm.add_widget(BookWindow(name="BookWindow"))
        sm.add_widget(Comments(name="Comments"))

        return sm
        
    


if __name__ == '__main__':
    MyApp().run()