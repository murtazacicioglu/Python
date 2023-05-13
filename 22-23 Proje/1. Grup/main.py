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

    e = engine.Engine()
    e.load_source_code(icerik)
    print("Kod, belleğe yüklendi")
    print(f"İşlemci frekansı: {e.get_frequency()} Hz")
    e.run()


if __name__ == "__main__":
    main()
