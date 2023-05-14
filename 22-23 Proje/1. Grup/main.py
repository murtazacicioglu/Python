#!/usr/bin/env python
#
#       Ferit Yiğit BALABAN, <fybalaban@fybx.dev>
#
#       main.py
import sys
import engine


def main():
    print("RISC-Mini: PPG 1. Grup Proje Ödevi")
    print("-" * 34)
    print("Damla SOYDAN", "İrem İÇÖZ", "Ferit Yiğit BALABAN", "Sabir SÜLEYMANLI", "Zeynep KILINÇER", sep="\n", end="\n")
    print("-" * 34)
    print("Seçtiğiniz dosya okunur, parse edilir ve RAM'e yüklenir. Kod RAM'den yürütülür.")
    print("Kaynak kodu içeren dosyayı "
          "\n- \'python main.py kod.asm\' veya"
          "\n- \'main.py kod.asm\' şeklinde sağlayabilirsiniz.")

    sys.argv = sys.argv[1:]
    if len(sys.argv) == 0:
        print("Dosya komut argümanı olarak verilmemiş.")
        yol = input("Lütfen çalıştırılacak dosyanın konumunu giriniz: ")
    else:
        yol = sys.argv[0]

    try:
        with open(yol, "r") as f:
            icerik = f.read()
    except FileNotFoundError:
        print(f"{yol} yolunda dosya bulunamadı")

    e = engine.Engine(None, "tui")
    e.load_source_code(icerik)
    print("[Engine] Kod, belleğe yüklendi")
    print(f"[Engine] İşlemci frekansı: {e.get_frequency()} Hz")
    r, d = e.get_debug()
    print(f"Debug secenekleri: ", 
          f"\n1. Yazmaclar:        {'yaz' if r else 'yazma'}",
          f"\n2. Komut isaretcisi: {'yaz' if d else 'yazma'}"
    )
    print("Debug modunu 0,0 formatinda veriniz")
    r, d = input("> ").split(",", maxsplit=1) # unpack hatasi almamak icin maxsplit verdim
    e.set_debug(r == "1", d == "1")
    print("Kod HALT edene dek çalıştırabilir ya da adımlatabilirsiniz.")
    print("1. Adımla (stepping)")
    print("2. Çalıştır")
    secim = input("> ")
    if secim == "1":
        print("Adimlamak icin enter, halt icin h tusuna basiniz")
        while True:
            if input("") == "h":
                break
            if e.step() == -1:
                print(f"Islem sona erdi (durum kodu {e.result_code})")
                break
    elif secim == "2":
        e.run()


if __name__ == "__main__":
    main()
