from Kaynak import hocalar, hoca_ofis_zamanlari, hata, hoca_listesi
from datetime import datetime
from Menu import hoca_menu


def hoca():
    while True:
        hoca_menu()
        secenek = int(input("Bir Seçenek Giriniz: "))

        # 1.Randevu oluştur.
        if secenek == 1:
            if len(hocalar) == 0:
                print(" ")
                print("Listede herhangi bir Hoca bulunmamaktadır.")
                continue
            hoca_listesi()
            while True:
                print(" ")
                hoca_id_input = input("Hoca ID'sini seçiniz (çıkış:0): ")
                if hoca_id_input == '0':
                    break
                try:
                    hoca_id = int(hoca_id_input)
                    if hoca_id in range(1, len(hocalar) + 1):
                        hoca_sec = hocalar[hoca_id - 1]
                        print("Seçtiğiniz hoca: " + hoca_sec)
                        print(" ")
                        tarih_str = input("Ofiste bulunduğunuz tarihini giriniz (GG-AA-YYYY): ")
                        saat_str = input("Ofiste Bulunduğunuz saatini giriniz (HH:MM): ")
                        zaman_str = tarih_str + ' ' + saat_str
                        try:
                            datetime_obj = datetime.strptime(zaman_str, "%d-%m-%Y %H:%M")
                            hoca_ofis_zamani = datetime_obj.strftime("%d-%m-%Y %H:%M")  # Ör:12-05-2023 12:12
                            if hoca_ofis_zamani in hoca_ofis_zamanlari.get(hoca_sec, []):
                                print("Bu tarih zaten mevcuttur.")
                            else:
                                if hoca_sec not in hoca_ofis_zamanlari:
                                    hoca_ofis_zamanlari[hoca_sec] = []
                                hoca_ofis_zamanlari[hoca_sec].append(hoca_ofis_zamani)
                                print("Tarih oluşturuldu! Tarih: {}".format(hoca_ofis_zamani))
                                break
                        except ValueError:
                            print(" ")
                            print("Geçersiz tarih veya saat formatı. Lütfen doğru formatta tekrar deneyiniz.")
                    else:
                        hata()
                except ValueError:
                    hata()
        # 2. Geri Dön
        elif secenek == 2:
            break
        # Geçersiz giriş.
        else:
            hata()
