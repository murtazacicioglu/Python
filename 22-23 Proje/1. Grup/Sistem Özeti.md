## Sistem Özeti

![image](https://github.com/fybx/bmb2014/assets/41127439/efd836d4-0d1f-4da5-a5e2-bc6cb9651ad7)

## İşlemci

İşlemci `x0`'dan başlayarak `x31`'e kadar sıralanmış, 32 adet, 32-bit genişliğinde işaretli tam sayı tutan genel amaçlı yazmaca sahiptir.

Yazmaçların yanında `C`, `Z`, `S` ve `V` ile adreslenebilen bayrak yazmaçları yer almaktadır. Bayraklar da 32-bit genişliğindedir fakat yalnızca `0h` ve `1h` değerlerini saklamak için kullanılmalıdır.

### Bayraklar

| Bayrak Kısaltması | Açıklaması        |
|-------------------|-------------------|
| C                 | Elde (**c**arry)  |
| Z                 | Sıfır (**z**ero)  |
| S                 | İşaret (**s**ign) |
| V                 | Taşma (overflow)  |