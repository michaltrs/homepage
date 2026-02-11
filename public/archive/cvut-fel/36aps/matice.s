.data
	_N:	
		.word	5

	_MatrixA:
		.word         1,  2,  3,  4,  5
		.word         6,  7,  8,  9, 10
		.word        11, 12, 13, 14, 15
		.word        16, 17, 18, 19, 20
		.word        21, 22, 23, 24, 25
		.word         1,  2,  3,  4,  5
		.word         6,  7,  8,  9, 10
		.word        11, 12, 13, 14, 15
		.word        16, 17, 18, 19, 20
		.word        21, 22, 23, 24, 25
		.word         1,  2,  3,  4,  5
		.word         6,  7,  8,  9, 10
		.word        11, 12, 13, 14, 15
		.word        16, 17, 18, 19, 20
		.word        21, 22, 23, 24, 25
		.word         1,  2,  3,  4,  5
		.word         6,  7,  8,  9, 10
		.word        11, 12, 13, 14, 15
		.word        16, 17, 18, 19, 20
		.word        21, 22, 23, 24, 25

	_MatrixB:
      	.word        21, 1, 20, 11, 10
		.word        22, 2, 19, 12, 9
		.word        23, 3, 18, 13, 8
		.word        24, 4, 17, 14, 7
		.word        25, 5, 16, 15, 6
		.word        21, 1, 20, 11, 10
		.word        22, 2, 19, 12, 9
		.word        23, 3, 18, 13, 8
		.word        24, 4, 17, 14, 7
		.word        25, 5, 16, 15, 6
		.word        21, 1, 20, 11, 10
		.word        22, 2, 19, 12, 9
		.word        23, 3, 18, 13, 8
		.word        24, 4, 17, 14, 7
		.word        25, 5, 16, 15, 6
		.word        21, 1, 20, 11, 10
		.word        22, 2, 19, 12, 9
		.word        23, 3, 18, 13, 8
		.word        24, 4, 17, 14, 7
		.word        25, 5, 16, 15, 6

	_MatrixC:
		.word        0,0,0,0,0,0,0,0,0,0
		.word        0,0,0,0,0,0,0,0,0,0
		.word        0,0,0,0,0,0,0,0,0,0
		.word        0,0,0,0,0,0,0,0,0,0
		.word        0,0,0,0,0,0,0,0,0,0
		.word        0,0,0,0,0,0,0,0,0,0
		.word        0,0,0,0,0,0,0,0,0,0
		.word        0,0,0,0,0,0,0,0,0,0
		.word        0,0,0,0,0,0,0,0,0,0
		.word        0,0,0,0,0,0,0,0,0,0

	_Stack:	
		.space 400


; Pouzite registry
; R1: N
; R2: N div 4	
; R3: N mod 4

; R4, R5, R6, R7: radky v matrixA
; R8, R9, R10, R11: sloupce v matrixB

; R12: adresa programu pro mod

; R13: posunuti ve sloupci o 1 dolu (N*4)

; R14: Hlavni cyklus pocet radku v A
; R15: Cyklus pocet sloupcu v B
; R16: pocet opakovani divu
; R17: pozice v B
; R18: sloupec v B

; R23: adresa MatrixA
; R24: adresa MatrixB
; R25: adresa MatrixC

; Vysledky
; 5x5	- 1055	-	893
; 6x6	- 1705	-	1474
; 7x7	- 2428	-	2167
; 8x8	- 3465	-	3196
; 9x9	- 5274	-	4610
; 10x10	- 7089	-	6270



.text

_main:


  ; inicializace stacku + ulozeni registru

  	lhi	R29,((_Stack)>>16)&0xffff	
	addui	R29,R29,(_Stack)&0xffff	; 

	addui        r29, r29, 40
	sw           -40(r29), r4
  	sw           -36(r29), r5
  	sw           -32(r29), r6
  	sw           -28(r29), r7
  	sw           -24(r29), r16
  	sw           -20(r29), r17
  	sw           -16(r29), R18
  	sw           -12(r29), r23


	lhi		R23,((_MatrixA)>>16)&0xffff	; MatrixA
	addui	R23,R23,(_MatrixA)&0xffff	; 
	lhi		R24,((_MatrixB)>>16)&0xffff	; MatrixB
	addui	R24,R24,(_MatrixB)&0xffff	; 
	lhi		R25,((_MatrixC)>>16)&0xffff	; MatrixC
	addui	R25,R25,(_MatrixC)&0xffff	; 

	lw 		R1,_N
	srli 	R2,R1,#2			; N div 4
	andi 	R3,R1,#3			; N mod 4

	slli	R13,R1,#2			; posun na dalsi radek ve stejnem sloupci

	add		R14,R0,R1			; pocet opakovani hlavniho cyklu
	

; vypocet adresy programu pro provadeni N mod 4

	bnez	r3, zb1
	lhi		R12, ((ctyrikrat)>>16)&0xffff	; n mod 4 = 0
	addui	R12, R12, (ctyrikrat)&0xffff
	j		pokrac

zb1:	subi	r3, r3, #1
        bnez	r3, zb2
        lhi		R12, ((jednou)>>16)&0xffff	; n mod 4 = 1
        addui	R12, R12, (jednou)&0xffff
        j		pokrac

zb2:	subi	r3, r3, #1
        bnez	r3, zb3
        lhi		R12, ((dvakrat)>>16)&0xffff	; n mod 4 = 2
        addui	R12, R12, (dvakrat)&0xffff
        j		pokrac

zb3:	lhi		R12,((trikrat)>>16)&0xffff		; n mod 4 = 3	
        addui	R12,R12,(trikrat)&0xffff

pokrac:


loop:	add		R18,R0,R24			; nastaveni matice B na zacatek
		add		R15,R0,R1			; pocet opakovani sloupcu B
		subi	R14,R14,#1			; dec hlavni cyklus
		jr		R12					; proved vetev MOD

trikrat:	lw		R4,0(R23)			; Nacteni casti matice A
			lw		R5,4(R23)
			lw		R6,8(R23)
	
	
	loopz3:	add		R17,R0,R18			; nastaveni na zacatek sloupce v B
			lw		R8,0(R17)			; Nacteni cati matice B a vynasobeni s A
			add		R17,R17,R13
			mult	R8,R8,R4
			lw		R9,0(R17)
			add		R17,R17,R13
			mult	R9,R9,R5
			lw		R10,0(R17)
			add		R17,R17,R13
			mult	R10,R10,R6	

			add		R8,R8,R9			; Secteni 	
			add		R8,R8,R10

			sw		0(R25),R8			; ulozeni casti vysledku do C
	
			subi	R15,R15,#1
			addui	R25,R25,#4			; dalsi policko v C
			addui	R18,R18,#4			; dalsi sloupec v B
	
			bnez	R15,loopz3
	
		addui	R23,R23,#12			; posun o 3 prvky v A
		sub		R25,R25,R13			; Navrat na zacatek radky v C
		addi	R18,R17,#4			; prvni sloupec matice B posunut dolu o MOD

		j		ctyrikrat



dvakrat:	lw	R4,0(R23)			; Nacteni casti matice A
			lw	R5,4(R23)
	
	
	loopz2:	add		R17,R0,R18			; nastaveni na zacatek sloupce v B

			lw		R8,0(R17)			; Nacteni cati matice B a vynasobeni s A
			add		R17,R17,R13
			mult	R8,R8,R4
			lw		R9,0(R17)
			add		R17,R17,R13
			mult	R9,R9,R5

			add	R8,R8,R9			; Secteni 	

			sw	0(R25),R8			; ulozeni casti vysledku do C
	
			subi	R15,R15,#1
			addui	R25,R25,#4			; dalsi policko v C
			addui	R18,R18,#4			; dalsi sloupec v B
	
			bnez	R15,loopz2

	addui	R23,R23,#8			; posun o 2 prvky v A
	sub		R25,R25,R13			; Navrat na zacatek radky v C
	addi	R18,R17,#4			; prvni sloupec matice B posunut dolu o MOD

	j		ctyrikrat



jednou:	lw	R4,0(R23)			; Nacteni casti matice A

	loopz1:	lw		R8,0(R18)			; Nacteni cati matice B a vynasobeni s A

			addui	R18,R18,#4			; dalsi sloupec v B
			mult	R8,R8,R4

			sw		0(R25),R8			; ulozeni casti vysledku do C
	
			subi	R15,R15,#1
			addui	R25,R25,#4			; dalsi policko v C
	
			bnez	R15,loopz1

		addui	R23,R23,#4			; posun o 1 prvek v A
		sub		R25,R25,R13			; Navrat na zacatek radky v C

		j		ctyrikrat


ctyrikrat:	; kde zacit v B je v R18
	
		add		R16,R0,R2			; pocet opakovani DIV vetve

	div:	add		R15,R0,R1			; pocet opakovani sloupcu B

			lw		R4,0(R23)			; nacteni matice A
			lw		R5,4(R23)
			lw		R6,8(R23)
			lw		R7,12(R23)
			addi	R23,R23,#16			; posun o div , resp na dalsi radek (pro dalsi pruchod)

			ls:	add		R17,R0,R18			; nastaveni B
	
				lw		R8,0(R17)			; Nacteni matice B + vynasobeni
				add		R17,R17,R13
				mult	R8,R8,R4
				lw		R9,0(R17)
				add		R17,R17,R13
				mult	R9,R9,R5
				lw		R10,0(R17)
				add		R17,R17,R13
				mult	R10,R10,R6
				lw		R11,0(R17)
				add		R17,R17,R13
				mult	R11,R11,R7
	
				add 	R8,R8,R9			; soucet

				lw		R9,0(R25)   ; nacteni jiz ulozeneho C

				add		R8,R8,R10	
				add		R8,R8,R11	

				add		R8,R8,R9			; soucet s puvodnim C

				sw		0(R25),R8

				subi	R15,R15,#1			; pocet sloupcu B - 1
				addui	R25,R25,#4			; dalsi sloupec v C
				addui	R18,R18,#4			; dalsi sloupec v B

				bnez	R15,ls

			subi	R16,R16,#1			; dec DIV cyklu
	
			sub		R25,R25,R13			; zacatek radku v C
			add		R18,R17,#4			; zacatek dalsi radky B
			bnez 	R16,div
	
		add		R25,R25,R13			; dalsi radek v C
		bnez	R14,loop			; hlavni cyklus


  	; nacteni registru ze zasobniku
  	lw           r4, -40(r29)
  	lw           r5, -36(r29)
  	lw           r6, -32(r29)
  	lw           r7, -28(r29)
  	lw           r16, -24(r29)
  	lw           r17, -20(r29)
  	lw           R18, -16(r29)
  	lw           r23, -12(r29)
  	subui        r29, r29, 40

	trap	#0
