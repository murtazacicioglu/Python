## RISC-Mini Dokümanları

### Çağrılar

#### Sistemi Durdur (HALT)

| Yazmaç | Beklenen Değer |
|--------|----------------|
| `x1`   | `0`            |

#### Ekrana Yazmaç Değeri Yazdır

| Yazmaç | Beklenen Değer                                      |
|--------|-----------------------------------------------------|
| `x1`   | `1`                                                 |
| `x2`   | Bu yazmaçtaki değer ekrana yazılacak.               |
| `x3`   | Sayı formatı (`0`: ikili; `1`: onlu; `2`: onaltılı) |

#### Ekrana String Yazdır

| Yazmaç | Beklenen Değer             |
|--------|----------------------------|
| `x1`   | `2`                        |
| `x2`   | Stringin bellekteki adresi |
