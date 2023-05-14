## RISC-Mini Dokümanları

### Çağrılar

#### Sistemi Durdur (HALT)

| Yazmaç | Beklenen Değer |
|--------|----------------|
| `x1`   | `0`            |

#### Ekrana Yazmaç Değeri Yazdır

| Yazmaç | Beklenen Değer                                                 |
|--------|----------------------------------------------------------------|
| `x1`   | `1`                                                            |
| `x2`   | Bu yazmaçtaki değer ekrana yazılacak.                          |
| `x3`   | Sayı formatı (`0`: ikili; `1`: onlu; `2`: onaltılı; `3`: utf8) |

#### Ekrana String Yazdır

| Yazmaç | Beklenen Değer             |
|--------|----------------------------|
| `x1`   | `2`                        |
| `x2`   | Stringin bellekteki adresi |

#### Klavyeden Karakter Oku

| Yazmaç | Beklenen Değer                         |
|--------|----------------------------------------|
| `x1`   | `3`                                    |
| `x2`   | Karakterin kaydedileceği bellek adresi |

#### Klavyeden Girilen Stringi Oku

Okunan karakterin UTF-8 kodlama sisteminde numerik degerini `x3` yazmacindaki degere gore ya `x4` yazmacina kaydeder ya da `x2` yazmacinda verilen bellek adresine kaydeder. Bellege yazma durumunda hedef kayit adresinden sonraki adrese `0` yazilacagina dikkat edilmelidir.

| Yazmaç | Beklenen Değer                                                                 |
|--------|--------------------------------------------------------------------------------|
| `x1`   | `4`                                                                            |
| `x2`   | Karakterin kaydedileceği bellek bloğunun başlangıç adresi                      |
| `x3`   | Kayit konumunu secer (`0`: `x4` yazmaci; `1`: `x2` yazmacindaki bellek adresi) |

#### Klavyeden Sayi Oku

Verilen sayi kabul formatina gore okunan karakter dizisini sayiya cevirir ve `x3` yazmacinda saklar. Eger sayi verilen formatta okunamiyorsa `x4` yazmacina `1` degeri kaydedilir.

| Yazmaç | Beklenen Değer                                            |
|--------|-----------------------------------------------------------|
| `x1`   | `5`                                                       |
| `x2`   | Sayi kabul formati (`0`: ikili; `1`: onlu: `2`: onaltili) |

