from Kaynak import ogr_randevulari, hata, hoca_listesi, hocalar, hoca_ofis_zamanlari
from Menu import ogr_menu


def ogr():
    while True:
        # ---Menü---
        ogr_menu()
        # ---Giriş---
        try:
            secenek = int(input("Bir Seçenek Giriniz: "))
        except ValueError:
            hata()
            continue
        # ---1. Randevu Al---
        if secenek == 1:
            if len(hocalar) == 0:
                print(" ")
                print("Listede herhangi bir Hoca bulunmamaktadır.")
                continue
            hoca_listesi()
            while True:
                print(" ")
                try:
                    hoca_id = int(input("Hoca ID'sini seçiniz (iptal:0): "))
                except ValueError:
                    hata()
                    continue
                if hoca_id == 0:
                    break
                if hoca_id in range(1, len(hocalar) + 1):
                    hoca_sec_ogr = hocalar[hoca_id - 1]
                    print("Seçtiğiniz hoca: " + hoca_sec_ogr)
                    randevulari = hoca_ofis_zamanlari.get(hoca_sec_ogr, [])
                    if len(randevulari) > 0:
                        print("Uygun randevuları: ")
                        for i, randevu in enumerate(randevulari):
                            print(f"{i + 1}. {randevu}")
                        randevu_secimi = int(input("Bir randevu seçiniz (iptal: 0): "))
                        if randevu_secimi == 0:
                            continue
                        if randevu_secimi in range(1, len(randevulari) + 1):
                            secilen_randevu = randevulari[randevu_secimi - 1]
                            if secilen_randevu in ogr_randevulari.values():
                                print("Bu randevuyu zaten almışsınız. Başka bir tarih seçiniz.")
                            else:
                                ogr_randevulari[hoca_sec_ogr] = secilen_randevu
                                print("Randevu alındı! Tarih: {}".format(secilen_randevu))
                                break
                        else:
                            hata()
                    else:
                        print("Bu hocanın mevcut randevusu bulunmamaktadır.")
                else:
                    hata()
        # ---2. Randevularımı Görüntüle---
        elif secenek == 2:
            if len(ogr_randevulari) == 0:
                print(" ")
                print("Henüz randevu almamışsınız.")
                continue
            print(" ")
            print("Aldığınız randevular:")
            for i, (hoca_adi, randevu) in enumerate(ogr_randevulari.items(), start=1):
                print(f"{i}. Hoca: {hoca_adi} - Zaman: {randevu}")
        # ---3. Geri Dön---
        elif secenek == 3:
            break
        # ---Hata---
        else:
            hata()
