;
; 		Ferit Yigit BALABAN,	<fybalaban@fybx.dev>
;		RISC-Mini,		2023
;		toplama.asm

.global
	mvi x9, Ah	; x9 yazmacinda yeni satir karakterini tut

	mvi x1, 5h	; syscall no.5 hazirligi
	mvi x2, 1h	; sayiyi onlu sistemde oku
	cll		; cagriyi gerceklestir
	mov x20, x3	; okunan sayiyi x20'de sakla

	mvi x1, 2h	; syscall no.2 hazirligi
	mvi x2, [str0]	; ekrana yazilacak stringin adresini sakla
	cll		; cagriyi gerceklestir

	mvi x1, 5h	; syscall no.5 hazirligi
	mvi x2, 1h	; sayiyi onlu sistemde oku
	cll		; cagriyi gerceklestir
	mov x21, x3	; okunan sayiyi x21'de sakla

	mvi x1, 2h	; syscall no.2 hazirligi
	mvi x2, [str1]	; ekrana yazilacak stringin adresini sakla
	cll		; cagriyi gerceklestir

	mvi x1, 1h		; syscall no.1 hazirligi
	add x2, x20, x21	; ekrana yazilacak sayiyi (toplami) x2'de sakla
	mvi x3, 1h		; sayiyi onlu sistemde yaz
	cll			; cagriyi gerceklestir

	mvi x1, 2h	; syscall no.2 hazirligi
	mov x2, x9	; yeni satir karakterini sakla
	cll		; cagriyi gerceklestir

	mov x1, x0	; islemciyi durdur
	mov x2, x0	; durum kodu 0
	cll

.store
	dbs str0, " + "
	dbs str1, " = "
