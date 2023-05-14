from Kaynak import hocalar, hoca_listesi, hata
from Kaynak import hoca_ekle, hoca_sil
from Menu import yonetici_menu


def yonetici():
    while True:
        # ---Menü---
        yonetici_menu()
        hoca_listesi()
        print(" ")
        # ---Giriş---
        try:
            secenek = int(input("Bir seçenek giriniz: "))
        except ValueError:
            hata()
            continue
        # ---1. Hoca Ekle---
        if secenek == 1:
            hoca_ismi = input("Eklemek istediğiniz hoca ismi giriniz (iptal: q): ")
            if hoca_ismi.lower() == 'q':
                continue
            if hoca_ismi in hocalar:
                print(" ")
                print("**Hoca listede zaten vardır!")
            else:
                hoca_ekle(hoca_ismi)
        # ---2. Hoca Sil---
        elif secenek == 2:
            if len(hocalar) == 0:
                print(" ")
                print("Listede herhangi bir Hoca bulunmamaktadır.")
                continue
            try:
                hoca_id = int(input("Listeden silmek istediğiniz hoca numarası (iptal: 0): "))
            except ValueError:
                hata()
                continue
            if hoca_id == 0:
                continue
            hoca_sil(hoca_id)
        # ---3. Geri Dön---
        elif secenek == 3:
            break
        # ---Hata---
        else:
            hata()
            continue




