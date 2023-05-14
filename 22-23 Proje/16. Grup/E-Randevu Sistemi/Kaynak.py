hocalar = []
hoca_ofis_zamanlari = {}
ogr_randevulari = {}


def hoca_listesi():
    print("======== HOCA LİSTESİ ========")
    for i, hoca_adi in enumerate(hocalar):
        print(f"{i + 1}. {hoca_adi}")
    print("==============================")


def hata():
    print(" ")
    print("**Geçersiz giriş. Lütfen tekrar deneyiniz.")


def hoca_ekle(ad):
    if not ad.isalpha():
        hata()
    else:
        hocalar.append(ad)
        hoca_ofis_zamanlari[ad] = []
        print(" ")
        print("Hoca listeye başarıyla Eklendi!")


def hoca_sil(hoca_num):
    if hoca_num in range(1, len(hocalar) + 1):
        hoca_adi = hocalar[hoca_num - 1]
        hocalar.remove(hoca_adi)
    else:
        hata()
    for i, listedeki_hoca in enumerate(hocalar):
        split = listedeki_hoca.split('. ', 1)
        if len(split) >= 2:
            hocalar[i] = f"{i + 1}. {split[1]}"
