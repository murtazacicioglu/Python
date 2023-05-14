;
;       Ferit Yiğit BALABAN,    <fybalaban@fybx.dev>
;       RISC-Mini               2023
;       merhaba_dunya.asm

.global
    mvi x1, 2h
    mvi x2, [str]
    cll
    mov x1, x0
    mov x2, x0
    cll

.store
    dbs str, "Merhaba, Dünya!"
