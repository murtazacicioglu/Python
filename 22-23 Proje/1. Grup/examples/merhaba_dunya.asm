;
;       Ferit Yiğit BALABAN,    <fybalaban@fybx.dev>
;       RISC-Mini               2023
;       merhaba_dunya.asm

.global
    mvi x1, 11h
    mvi x2, [str]
    cll
    mov x1, x0
    cll

.store
    dbs str, "Merhaba, Dünya!"
