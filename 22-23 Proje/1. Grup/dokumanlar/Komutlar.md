## Kabul Edilen Komutlar

### Aritmetik Komutları

| Mnemonik | Sentaks            | Açıklama                               |
|----------|--------------------|----------------------------------------|
| add      | `add rd, rs1, rs2` | `rd` ← (`rs1` + `rs2`)                 |
| inv      | `inv rd`           | `rd` ← (-1 * `rd`)                     |
| sub      | `sub rd, rs1, rs2` | `rd` ← (`rs1` - `rs2`)                 |
| slt      | `slt rd, rs1, rs2` | `rd` ← (`rs1` < `rs2` ? `rs1` : `rs2`) |
| nop      | `nop`              | `x0` ← `x0`                            |

### Bellek Komutları

| Mnemonik | Sentaks                | Açıklama                                                               |
|----------|------------------------|------------------------------------------------------------------------|
| `lfm`    | `lfm rd, [hex_value]h` | Belleğin `hex_value` adresinde yer alan değerini `rd` yazmacına yükler |
| `stm`    | `stm rd, [hex_value]h` | Belleğin `hex_value` adresinde `rd` yazmacındaki değeri saklar         |
| `mov`    | `mov rd, rs1`          | `rd` ← `rs1`                                                           |
| `mvi`    | `mvi rd, [hex_value]h` | `rd` ← `hex_value`                                                     |

### Mantıksal Komutlar

| Mnemonik | Sentaks            | Açıklama                |
|----------|--------------------|-------------------------|
| `and`    | `and rd, rs1, rs2` | `rd` ← (`rs1` & `rs2`)  |
| `or`     | `or rd, rs1, rs2`  | `rd` ← (`rs1` \| `rs2`) |
| `xor`    | `xor rd, rs1, rs2` | `rd` ← (`rs1` ^ `rs2`)  |
| `shl`    | `shl rd, rs1, rs2` | `rd` ← (`rs1` << `rs2`) |
| `shr`    | `shr rd, rs1, rs2` | `rd` ← (`rs1` >> `rs2`) |

### Dallanma Komutları

| Mnemonik | Sentaks                 | Açıklama                                                     |
|----------|-------------------------|--------------------------------------------------------------|
| `jmp`    | `jmp section`           | `x30` yazmacına program sayacını kaydederek `section`a atlar |  
| `beq`    | `beq rs1, rs2, section` | `rs1` == `rs2` ? `jmp section` : `nop`                       |
| `bne`    | `bne rs1, rs2, section` | `rs1` != `rs2` ? `jmp section` : `nop`                       |
| `bge`    | `bge rs1, rs2, section` | `rs1` >= `rs2` ? `jmp section` : `nop`                       |
| `ble`    | `ble rs1, rs2, section` | `rs1` <= `rs2` ? `jmp section` : `nop`                       |


### Ek

| Mnemonik | Sentaks                      | Açıklama                                                                                     |
|----------|------------------------------|----------------------------------------------------------------------------------------------|
| `cll`    | `cll`                        | Sistem çağrısı yapar. Detaylar için `Çağrılar.md` dosyasını okuyunuz                         |
| `dbs`    | `dbs name \"quoted_string\"` | Bellekte `name` adıyla referans verilebilen bir null-sonlandırmalı karakter dizisi kaydeder. |