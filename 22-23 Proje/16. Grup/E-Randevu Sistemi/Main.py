from Yonetici import yonetici
from Hoca import hoca
from Ogr import ogr
from Kaynak import hata
from Menu import ana_menu


def main():
    while 1:
        ana_menu()
        fonksiyolar = 4
        try:
            kullanici = int(input("Bir seçenek giriniz: "))
            if kullanici not in range(1, fonksiyolar + 1):
                hata()
            else:
                if kullanici == 1:
                    yonetici()
                if kullanici == 2:
                    hoca()
                if kullanici == 3:
                    ogr()
                if kullanici == 4:
                    break
        except ValueError:
            hata()
            continue


if __name__ == "__main__":
    main()
